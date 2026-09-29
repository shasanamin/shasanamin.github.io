# A smaller academic website

The code behind [my website](https://shasanamin.github.io). I started with [al-folio](https://github.com/alshedivat/al-folio) and rebuilt it around what I actually use. The aim was to benefit from the visual character while making the site much easier to understand and maintain.

It is also a starting point for researchers and other professionals who want their work to be easy to browse. Publications have illustrations, PDF/code links, and copyable BibTeX. There are light and dark themes, a mobile layout, and a small “gold nuggets” feature for a little personality. Most updates mean editing a few lines of Markdown or YAML.

The stack is Jekyll, plain CSS, and a little JavaScript. No frontend framework or image-processing tools are needed to build it.

## Where things live

| To update… | Edit… |
| --- | --- |
| Name, links, portrait, site address, homepage limits | `_config.yml` |
| Introduction and other pages | `pages/` |
| News, publications, service | `_data/` |
| Files including CV, photos and PDFs | `files/` |
| Colors, typography, and spacing | `assets/site.css` |
| Page structure and reusable components | `_layouts/` and `_includes/` |

Copy an existing data entry when adding news or a paper. News sorts by date, while publications follow file order. The homepage shows the latest five announcements and the first ten papers marked `selected: true`. Replace `files/cv.pdf` to update the CV. Add a Markdown file in `pages/` with a `title`, `permalink`, and `nav: true` to add a page to navigation.

## Make it yours

Fork or copy the repository, then replace my information and uploads with yours. Start with `_config.yml` and `pages/index.md`, followed by the data files. Set `url` to your domain and `baseurl` to your project path, if any. The CSS variables at the top of `assets/site.css` are the place to give it your own visual identity.

An AI coding assistant can help with the initial migration. Give it this repository and your CV or existing website, then try:

> Adapt this site for me using the attached CV and my existing website as factual sources. Keep its simple structure and make the writing sound like me. Update the biography, publications, news, service, contact links, and uploads; remove sections I do not need. Preserve publication status and author order, verify paper links, and flag missing information rather than inventing it. Keep routine updates in Markdown and YAML. Check both themes, mobile layouts, local links, and the build. Leave me a brief list of what changed and anything I need to confirm before publishing.

Keep private source material outside the public files.

## Preview and publish

Use Ruby **3.3.6** (see `.ruby-version`) and Bundler:

```sh
bundle install
bundle exec jekyll serve
```

Open [localhost:4000](http://localhost:4000). Restart the server after changing `_config.yml`.

Before pushing, with Python 3 also available:

```sh
bundle exec ruby scripts/test_site.rb
bundle exec jekyll build
python3 scripts/check_site.py _site
```

The GitHub workflow checks both root and subpath builds, then publishes successful pushes to `main` or `master` to `gh-pages`. Set GitHub Pages to serve that branch. Pull requests run checks without publishing.

## Credits and reuse

The site retains elements of [al-folio](https://github.com/alshedivat/al-folio), © 2022 Maruan Al-Shedivat, originally based on Lia Bogoev’s [*folio](https://github.com/bogoli/-folio). The code is available under the [MIT license](LICENSE); keep that notice when reusing it. Personal materials and paper PDFs retain their own rights and licenses.

- Social and theme glyphs are adapted from [Font Awesome Free 6.4.0](https://github.com/FortAwesome/Font-Awesome/blob/6.4.0/LICENSE.txt), © 2023 Fonticons, Inc., and the Google Scholar glyph from [Academicons 1.9.4](https://github.com/jpswalsh/academicons/blob/v1.9.4/svg/google-scholar.svg), James Walsh. Both projects license SVG icons under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Packaging and sizing were adapted; the Scholar glyph’s additional OFL notice is retained in `_includes/icon.html`. Brand marks belong to their owners.
- [Crimson Pro](https://github.com/google/fonts/blob/main/ofl/crimsonpro/OFL.txt), © 2018 the Crimson Pro Project Authors, and [Noto Nastaliq Urdu](https://github.com/google/fonts/blob/main/ofl/notonastaliqurdu/OFL.txt), © 2022 the Noto Project Authors, are loaded from Google Fonts under SIL OFL 1.1.
- Section icons and the favicon were made for this site. Publication illustrations were generated with OpenAI’s image tool to explain research concepts; [artwork notes](scripts/publication-art.md) describe them.
