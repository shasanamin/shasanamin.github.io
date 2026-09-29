#!/usr/bin/env python3
"""Check a Jekyll build using Python's standard library and Ruby's YAML reader."""

import argparse
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import subprocess
import sys
from urllib.parse import unquote, urljoin, urlsplit


class Element:
    def __init__(self, tag="", attrs=()):
        self.tag = tag
        self.attrs = dict(attrs)
        self.children = []

    def find(self, tag=None, css_class=None):
        for child in self.children:
            if isinstance(child, Element):
                if (tag is None or child.tag == tag) and (
                    css_class is None or css_class in child.attrs.get("class", "").split()
                ):
                    yield child
                yield from child.find(tag, css_class)

    def text(self):
        return " ".join(
            "".join(c.text() if isinstance(c, Element) else c for c in self.children).split()
        )


class Document(HTMLParser):
    VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr"}

    def __init__(self, source):
        super().__init__(convert_charrefs=True)
        self.root = Element()
        self.stack = [self.root]
        self.feed(source)

    def handle_starttag(self, tag, attrs):
        node = Element(tag, attrs)
        self.stack[-1].children.append(node)
        if tag not in self.VOID:
            self.stack.append(node)

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in self.VOID:
            self.handle_endtag(tag)

    def handle_endtag(self, tag):
        for index in range(len(self.stack) - 1, 0, -1):
            if self.stack[index].tag == tag:
                self.stack = self.stack[:index]
                break

    def handle_data(self, data):
        self.stack[-1].children.append(data)


def read_site_data(source):
    # Ruby is already required to build the site; avoid a separate Python YAML dependency.
    code = """
      data = ARGV.to_h do |file|
        [File.basename(file, '.yml'), YAML.safe_load_file(file, permitted_classes: [Date, Time], aliases: true)]
      end
      puts JSON.generate(data)
    """
    paths = [source / "_config.yml"] + [source / "_data" / f"{name}.yml" for name in ("news", "publications", "nuggets", "service")]
    result = subprocess.run(
        ["ruby", "-rjson", "-rdate", "-ryaml", "-e", code, *map(str, paths)],
        text=True, capture_output=True, check=True,
    )
    return json.loads(result.stdout)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("destination", nargs="?", default="_site")
    parser.add_argument("--baseurl", help="Build subpath, e.g. /preview (defaults to _config.yml)")
    args = parser.parse_args()
    destination = Path(args.destination).resolve()
    source = Path(__file__).resolve().parent.parent
    data = read_site_data(source)
    configured_baseurl = args.baseurl if args.baseurl is not None else data["_config"].get("baseurl", "")
    baseurl = "/" + configured_baseurl.strip("/") if configured_baseurl.strip("/") else ""
    origin = data["_config"]["url"].rstrip("/")
    errors = []

    def check(condition, message):
        if not condition:
            errors.append(message)

    def public_url(path):
        return baseurl + "/" + path.lstrip("/")

    def local_file(url, current="/"):
        resolved = urlsplit(urljoin(origin + current, url))
        if resolved.scheme not in ("http", "https") or resolved.netloc != urlsplit(origin).netloc:
            return None, None
        path = unquote(resolved.path)
        if baseurl and path != baseurl and not path.startswith(baseurl + "/"):
            errors.append(f"URL escapes baseurl {baseurl}: {url} (from {current})")
            return None, None
        path = path[len(baseurl):] if baseurl else path
        target = (destination / path.lstrip("/")).resolve()
        if not target.is_relative_to(destination):
            errors.append(f"URL escapes the output directory: {url}")
            return None, None
        if target.is_dir() or path.endswith("/"):
            target = target / "index.html"
        return target, unquote(resolved.fragment)

    html_files = sorted(destination.rglob("*.html"))
    check(bool(html_files), f"No HTML build found at {destination}")
    documents = {path: Document(path.read_text()).root for path in html_files}
    obsolete = re.compile(r"jquery|bootstrap|(?:^|/)mdb(?:[./-]|$)|mathjax|fontawesome|academicons|distillpub|medium-zoom", re.I)
    expected_icons = {public_url(data["_config"][key]) for key in ("icon", "icon_fallback")}
    favicon = destination / "favicon.ico"
    favicon_source = source / data["_config"]["icon_fallback"].lstrip("/")
    check(favicon.is_file() and favicon.read_bytes() == favicon_source.read_bytes(),
          "Root favicon.ico must contain the current configured ICO bytes")
    for path, document in documents.items():
        relative = path.relative_to(destination).as_posix()
        route = "/" + (relative[:-10] if relative.endswith("index.html") else relative)
        current = public_url(route)
        ids = [node.attrs["id"] for node in document.find() if "id" in node.attrs]
        check(len(ids) == len(set(ids)), f"Duplicate HTML id in {relative}")
        icons = {node.attrs.get("href") for node in document.find("link")
                 if "icon" in node.attrs.get("rel", "").split()}
        check(icons == expected_icons, f"Missing or outdated favicon declarations in {relative}")
        for node in document.find():
            if node.tag == "img":
                check("alt" in node.attrs, f"Image has no alt attribute in {relative}")
            urls = [node.attrs[attr] for attr in ("href", "src") if node.attrs.get(attr)]
            urls += [part.strip().split()[0] for part in node.attrs.get("srcset", "").split(",") if part.strip()]
            for url in urls:
                if node.tag in ("script", "link"):
                    check(not obsolete.search(url), f"Obsolete library in {relative}: {url}")
                target, fragment = local_file(url, current)
                if target is None:
                    continue
                check(target.is_file(), f"Missing target in {relative}: {url}")
                if fragment and target in documents:
                    target_ids = {n.attrs.get("id") for n in documents[target].find()}
                    target_ids |= {n.attrs.get("name") for n in documents[target].find("a")}
                    check(fragment in target_ids, f"Missing fragment in {relative}: {url}")

    for route in ("/", "/publications/", "/service/", "/news/", "/404.html"):
        target, _ = local_file(public_url(route))
        check(target in documents, f"Missing active route {route}")

    def page(route):
        target, _ = local_file(public_url(route))
        return documents.get(target, Element())

    def news_rows(document):
        return [row for table in document.find("table", "news") for row in table.find("tr")]

    # The collection stays editable in YAML and renders without JavaScript. The
    # homepage disclosure reveals one original-language quote; there is no details page.
    nuggets = data["nuggets"] or []
    check(isinstance(nuggets, list) and bool(nuggets), "nuggets.yml must contain a nonempty list")
    nugget_ids = []
    for entry in nuggets if isinstance(nuggets, list) else []:
        check(isinstance(entry, dict), "Every nugget must be a record")
        if not isinstance(entry, dict):
            continue
        identifier = entry.get("id")
        check(isinstance(identifier, str) and bool(re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", identifier)), f"Invalid nugget id: {identifier}")
        nugget_ids.append(identifier)
        check(isinstance(entry.get("text"), str) and bool(entry["text"].strip()), f"Nugget needs text: {identifier}")
        check(isinstance(entry.get("lang"), str) and bool(re.fullmatch(r"[a-z]{2,3}(?:-[A-Za-z0-9]+)*", entry["lang"])), f"Nugget needs a language code: {identifier}")
        check(entry.get("dir") in {"ltr", "rtl", "auto"}, f"Nugget needs text direction: {identifier}")
        if entry.get("lang") in {"ur", "ar"}:
            check(entry.get("dir") == "rtl", f"Arabic-script nugget must read right to left: {identifier}")
    check(len(nugget_ids) == len(set(map(str, nugget_ids))), "Nugget ids must be unique")
    pockets = list(page("/").find("div", "nugget-pocket"))
    check(len(pockets) == 1, "Homepage must contain one Gold Nuggets discovery")
    check(not list(page("/").find("dialog")), "Homepage nuggets must reveal inline without a dialog")
    embedded = [node for node in page("/").find("script") if node.attrs.get("id") == "nugget-data"]
    check(len(embedded) == 1 and embedded[0].attrs.get("type") == "application/json", "Homepage must embed one JSON nugget collection")
    if embedded:
        try:
            rendered_nuggets = json.loads("".join(child for child in embedded[0].children if isinstance(child, str)))
            check(rendered_nuggets == nuggets, "Embedded nuggets must preserve the YAML collection, including Unicode and line breaks")
        except ValueError:
            check(False, "Embedded nugget collection is not valid JSON")
    if pockets:
        disclosure = next(pockets[0].find("details"), Element())
        trigger = next(disclosure.find("summary"), Element())
        check(bool(trigger.attrs.get("aria-label")), "Image-only nugget trigger needs an accessible name")
        check(not trigger.text(), "Nugget artwork must not have visible invitation text")
        check(not list(pockets[0].find("button")), "Nugget discovery must not add category or navigation buttons")
        original = next(disclosure.find("blockquote"), Element())
        if isinstance(nuggets, list) and nuggets and isinstance(nuggets[0], dict):
            first = nuggets[0]
            check(original.text() == " ".join(first.get("text", "").split()), "No-JavaScript nugget must contain the first original text")
            check(original.attrs.get("lang") == first.get("lang") and original.attrs.get("dir") == first.get("dir", "auto"), "Fallback nugget must preserve its language and direction")
            check(not list(disclosure.find("a")), "Nuggets must not have translation or context links")
        artwork = list(pockets[0].find("img"))
        check(len(artwork) == 1, "Nugget invitation must have one illustration")
        if artwork:
            target, _ = local_file(artwork[0].attrs.get("src", ""))
            header = target.read_bytes()[:30] if target and target.is_file() else b""
            check(header[:4] == b"RIFF" and header[8:16] == b"WEBPVP8X", "Nugget illustration must be an extended WebP image")
            if len(header) == 30 and header[12:16] == b"VP8X":
                dimensions = tuple(1 + int.from_bytes(header[offset:offset + 3], "little") for offset in (24, 27))
                check(tuple(artwork[0].attrs.get(key) for key in ("width", "height")) == tuple(map(str, dimensions)), "Nugget illustration dimensions must match its file")
            check(artwork[0].attrs.get("alt") == "", "Nugget illustration must be decorative beside its named trigger")
    check(not (destination / "nuggets").exists(), "The removed nugget details page must not be generated")
    for route in ("/publications/", "/service/", "/news/", "/404.html"):
        document = page(route)
        check(not list(document.find("div", "nugget-pocket")), f"Gold Nuggets must appear only on the homepage: {route}")
        check(not any("/assets/nuggets." in node.attrs.get(attr, "") for node in document.find() for attr in ("src", "href")), f"Unrelated page must not load nugget assets: {route}")

    news = sorted(data["news"] or [], key=lambda entry: entry["date"], reverse=True)
    archive_rows = news_rows(page("/news/"))
    home_rows = news_rows(page("/"))
    check(len(archive_rows) == len(news), f"Archive has {len(archive_rows)} entries, expected {len(news)}")
    limit = data["_config"].get("news_limit", 5)
    expected_home = news if limit is None else news[:limit]
    check(len(home_rows) == len(expected_home), f"Homepage has {len(home_rows)} news entries, expected {len(expected_home)}")
    check([row.text() for row in home_rows] == [row.text() for row in archive_rows[:len(home_rows)]], "Homepage news differs from the archive's newest entries")
    for entry, row in zip(news, archive_rows):
        dates = [time.attrs.get("datetime", "")[:10] for time in row.find("time")]
        check(dates == [entry["date"][:10]], f"Wrong date/order for news: {entry['date']}")
    publications = data["publications"] or []
    groups = list(dict.fromkeys(publication["group"] for publication in publications))
    sections = list(page("/publications/").find("section", "publication-group"))
    check([next(section.find("h2"), Element()).text() for section in sections] == groups, "Publication group headings/order changed")
    for group, section in zip(groups, sections):
        expected = [publication["id"] for publication in publications if publication["group"] == group]
        check([card.attrs.get("id") for card in section.find("article", "paper")] == expected, f"Wrong publication count/order in {group}")

    selected = [publication for publication in publications if publication.get("selected")][:data["_config"].get("publication_limit", 10)]
    grouped_publications = [publication for group in groups for publication in publications if publication["group"] == group]
    archive_cards = list(page("/publications/").find("article", "paper"))
    home_cards = list(page("/").find("article", "paper"))
    check([card.attrs.get("id") for card in home_cards] == [item["id"] for item in selected], "Wrong homepage publication count/order")
    for records, cards in ((grouped_publications, archive_cards), (selected, home_cards)):
        check(len(records) == len(cards), "Publication records and rendered cards differ in count")
        for publication, card in zip(records, cards):
            identifier = publication["id"]
            check(card.attrs.get("id") == identifier, f"Wrong publication identifier: {identifier}")
            title = next(card.find("h3"), Element())
            check(title.text() == publication["title"], f"Wrong publication title: {identifier}")
            if publication.get("venue_acronym"):
                venues = list(card.find("strong", "paper-venue"))
                check(len(venues) == 1 and venues[0].text() == f"({publication['venue_acronym']})", f"Missing venue emphasis: {identifier}")
            if publication.get("bibtex"):
                disclosures = list(card.find("details", "paper-bibtex"))
                check(len(disclosures) == 1 and "open" not in disclosures[0].attrs, f"BibTeX must start collapsed: {identifier}")
                citations = list(card.find("textarea", "bibtex-text"))
                check(len(citations) == 1 and citations[0].text() == " ".join(publication["bibtex"].split()), f"BibTeX changed during HTML rendering: {identifier}")
                if citations:
                    check("readonly" in citations[0].attrs and bool(citations[0].attrs.get("aria-label")), f"BibTeX needs a named, read-only text field: {identifier}")
                copy_buttons = list(card.find("button", "bibtex-copy"))
                check(len(copy_buttons) == 1 and "hidden" in copy_buttons[0].attrs, f"Copy button must progressively enhance the citation: {identifier}")
            expected_url = public_url(publication["url"]) if publication["url"].startswith("/") else publication["url"]
            check(any(link.attrs.get("href") == expected_url for link in title.find("a")), f"Wrong paper link: {identifier}")
            check(all(author in card.text() for author in publication["authors"]), f"Missing authors: {identifier}")
            emphasized = [node.text() for node in card.find("span", "author-self")]
            check(emphasized == [author for author in publication["authors"] if author in data["_config"]["author_names"]], f"Wrong author emphasis: {identifier}")
            for field in ("venue", "location", "date", "award"):
                if publication.get(field):
                    check(publication[field] in card.text(), f"Missing {field}: {identifier}")
            if publication.get("figure"):
                figures = list(card.find("svg", "paper-figure"))
                check(len(figures) == 1, f"Publication must have one figure: {identifier}")
                if figures:
                    figure = figures[0]
                    check(figure.attrs.get("role") == "img" and figure.attrs.get("aria-label") == publication["figure_alt"], f"Missing accessible figure description: {identifier}")
                    check(figure.attrs.get("data-figure") == publication["figure"] and any(figure.find("path")), f"Figure did not render: {identifier}")
                    check(figure.attrs.get("viewbox") == "0 0 180 190", f"Wrong figure dimensions: {identifier}")
                check((source / "_includes/figures" / (publication["figure"] + ".svg")).is_file(), f"Missing figure source: {identifier}")
            else:
                images = list(card.find("img"))
                check(len(images) == 1, f"Publication must have one thumbnail: {identifier}")
                if images:
                    check(images[0].attrs.get("src") == public_url(publication["image"]) and images[0].attrs.get("alt") == publication.get("image_alt"), f"Wrong thumbnail or description: {identifier}")
                    check(bool(publication.get("image_alt", "").strip()), f"Empty thumbnail description: {identifier}")
                    check(all(images[0].attrs.get(attr) == str(publication.get("image_" + attr)) for attr in ("width", "height")), f"Thumbnail dimensions missing: {identifier}")
                    check(images[0].attrs.get("loading") == "lazy", f"Thumbnail should load lazily: {identifier}")
            links = list(card.find("a"))
            for field in ("pdf_url", "code_url"):
                if publication.get(field):
                    expected_link = public_url(publication[field]) if publication[field].startswith("/") else publication[field]
                    check(any(link.attrs.get("href") == expected_link for link in links), f"Missing {field}: {identifier}")
    archive_by_id = {card.attrs.get("id"): card for card in archive_cards}
    for card in home_cards:
        archive = archive_by_id.get(card.attrs.get("id"), Element())
        check(card.text() == archive.text(), f"Homepage and full-list citations differ: {card.attrs.get('id')}")
        check([link.attrs.get("href") for link in card.find("a")] == [link.attrs.get("href") for link in archive.find("a")], f"Homepage and full-list links differ: {card.attrs.get('id')}")

    figure_ids = [p.get("figure") or p.get("image") for p in publications]
    citation_keys = []
    for publication in publications:
        bibtex = publication.get("bibtex", "")
        match = re.match(r"\s*@(inproceedings|article|misc)\{([^,\s]+),", bibtex)
        check(bool(match), f"Missing or invalid BibTeX entry: {publication['id']}")
        if match:
            citation_keys.append(match.group(2))
        check(bibtex.count("{") == bibtex.count("}"), f"Unbalanced BibTeX braces: {publication['id']}")
        for field in ("title", "author", "year"):
            check(bool(re.search(r"\b" + field + r"\s*=", bibtex)), f"Missing BibTeX {field}: {publication['id']}")
        check(bool(publication.get("bibtex_source")), f"Missing citation provenance: {publication['id']}")
    check(len(citation_keys) == len(set(citation_keys)), "BibTeX keys must be unique")
    check(len(figure_ids) == len(set(figure_ids)), "Each publication must use a distinct figure")
    for publication in publications:
        if publication.get("image", "").endswith(".webp"):
            target, _ = local_file(public_url(publication["image"]))
            if target and target.is_file():
                header = target.read_bytes()[:30]
                # Our transparent WebP exports use the extended header. An RGB
                # image of a checkerboard must not silently replace real alpha.
                extended = (len(header) == 30 and header[:4] == b"RIFF"
                            and header[8:16] == b"WEBPVP8X")
                check(extended and bool(header[20] & 0x10),
                      f"Publication WebP needs an alpha channel: {publication['id']}")
                if extended:
                    dimensions = (1 + int.from_bytes(header[24:27], "little"),
                                  1 + int.from_bytes(header[27:30], "little"))
                    check(dimensions == (publication["image_width"], publication["image_height"]),
                          f"WebP size differs from declared dimensions: {publication['id']}")

    home_sections = [node.attrs.get("id") for node in page("/").find("section", "home-section")]
    check(home_sections == ["news", "research", "reviewing", "service"], "Homepage sections must follow intro, news, publications, reviewing, service")
    for publication in publications:
        if publication.get("pdf_url"):
            url = publication["pdf_url"]
            check(url.startswith("/files/") and url.endswith(".pdf"), f"Paper PDF must be local: {publication['id']}")
            pdf, _ = local_file(public_url(url))
            original = source / url.lstrip("/")
            check(pdf.is_file() and original.is_file() and pdf.read_bytes().startswith(b"%PDF-") and pdf.read_bytes() == original.read_bytes(), f"Invalid or changed PDF bytes: {publication['id']}")
        if publication.get("code_url"):
            check(urlsplit(publication["code_url"]).hostname == "github.com", f"Paper code must link to GitHub: {publication['id']}")
    for card in archive_cards + home_cards:
        resources = next(card.find("div", "paper-links"), Element())
        check(all(link.text().startswith(("PDF", "Code")) for link in resources.find("a")), f"Redundant publication resource link: {card.attrs.get('id')}")

    service = data["service"]
    home_service = next((node for node in page("/").find("section") if node.attrs.get("id") == "service"), Element())
    full_service = page("/service/")
    home_reviewing = next((node for node in page("/").find("section") if node.attrs.get("id") == "reviewing"), Element())
    for item in service["roles"]:
        for document in (full_service, home_service):
            check(all(str(item[field]) in document.text() for field in ("role", "organization", "years")), f"Service role missing: {item['role']} at {item['organization']}")
            expected = public_url(item["url"]) if item["url"].startswith("/") else item["url"]
            check(any(link.attrs.get("href") == expected for link in document.find("a")), f"Missing service link: {item['organization']}")
    for group in service["reviewing"]:
        for venue in group["venues"]:
            for document in (full_service, home_reviewing):
                matching = [node for node in document.find("li") if venue["full_name"] in node.text()]
                check(any(all(str(year) in node.text() for year in venue["years"]) and any(link.attrs.get("href") == venue["url"] for link in node.find("a")) for node in matching), f"Reviewing dates/link missing: {venue['name']}")
                if venue.get("recognition_years"):
                    check(any(all(str(year) in recognition.text() for year in venue["recognition_years"]) for node in matching for recognition in node.find("span", "review-recognition")), f"Missing reviewing recognition: {venue['name']}")
    check(not (destination / "assets/pdf").exists() and not (destination / "assets/img").exists(), "Retired asset aliases must not be generated")
    check(not any((destination / "news").glob("announcement*")), "Retired announcement pages must not be generated")

    refresh = [meta.attrs.get("content", "") for meta in page("/404.html").find("meta") if meta.attrs.get("http-equiv", "").lower() == "refresh"]
    check(any(re.fullmatch(r"3\s*;\s*url\s*=\s*" + re.escape(public_url("/")), value, re.I) for value in refresh), "404 must redirect home after three seconds")
    blocked = {"archived", "bkp", "cv-latex", "scripts", "_local", "_drafts", "_news", "_data", "_plugins", "vendor", "node_modules", "_projects"}
    for path in destination.rglob("*"):
        relative = path.relative_to(destination)
        check(
            not blocked.intersection(relative.parts)
            and not any("_local" in part or part.startswith("tmp_") for part in relative.parts),
            f"Private/build source leaked into output: {relative}",
        )
        check(path.name.lower() not in {"readme.md", "gemfile", "gemfile.lock", "example_pdf.pdf", "table_data.json", "resume.json"}, f"Template/build source leaked into output: {relative}")

    if errors:
        print("Site verification failed:", file=sys.stderr)
        for error in sorted(set(errors)):
            print(f"  - {error}", file=sys.stderr)
        return 1
    print(f"Verified {len(html_files)} HTML pages, {len(news)} announcements, {len(publications)} publications, {len(selected)} selected cards, {len(nuggets)} gold nuggets (baseurl={baseurl or '/'}).")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (OSError, subprocess.CalledProcessError, ValueError, KeyError) as error:
        print(f"Cannot verify site: {error}", file=sys.stderr)
        if isinstance(error, subprocess.CalledProcessError):
            print(error.stderr, file=sys.stderr)
        sys.exit(1)
