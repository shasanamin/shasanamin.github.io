# frozen_string_literal: true

# Focused regression checks for the small amount of custom Jekyll behavior.
# Run with: bundle exec ruby scripts/test_site.rb
require "jekyll"
require "tmpdir"
require "fileutils"
require "yaml"
require_relative "../_plugins/site"

class SiteChecks
  def initialize
    @assertions = 0
  end

  def run
    check_news
    check_errors
    check_filters
    puts "PASS: #{@assertions} custom Jekyll behavior checks"
  end

  private

  def assert(condition, message)
    @assertions += 1
    raise message unless condition
  end

  def entry(text, date = "2026-01-15")
    { "date" => date, "text" => text }
  end

  def with_site(news: :absent, baseurl: "/preview")
    Dir.mktmpdir("personal-site-check-") do |directory|
      source = File.join(directory, "source")
      destination = File.join(directory, "output")
      FileUtils.mkdir_p(File.join(source, "_layouts"))
      FileUtils.mkdir_p(File.join(source, "_includes"))
      FileUtils.mkdir_p(File.join(source, "_data"))
      # The shared layout prefixes internal links in page content.
      File.write(File.join(source, "_layouts/page.html"),
                 '<html><body><main data-layout="page">{{ content | local_links }}</main></body></html>')
      File.write(File.join(source, "index.html"), "---\nlayout: page\n---\n{% include news.html %}")
      FileUtils.cp(File.expand_path("../_includes/news.html", __dir__), File.join(source, "_includes"))
      File.write(File.join(source, "_data/news.yml"), news.to_yaml) unless news == :absent
      site = Jekyll::Site.new(Jekyll.configuration(
        "source" => source, "destination" => destination,
        "baseurl" => baseurl, "url" => "https://example.com",
        "cache_dir" => File.join(directory, "cache"),
        "quiet" => true, "plugins" => [], "timezone" => "UTC", "disable_disk_cache" => true
      ))
      site.process
      yield site, destination
    end
  end

  def check_news
    items = [entry("Old", "2025-01-01"), entry("First tied"),
             entry("Newest", "2026-02-01"), entry("Second tied")]
    with_site(news: items) do |site, _|
      assert(site.data["news"].map { |item| item["text"] } ==
             ["Newest", "First tied", "Second tied", "Old"],
             "News must sort newest first and preserve source order for equal dates")
    end

    [:absent, []].each do |items|
      with_site(news: items) do |site, output|
        assert(site.data["news"] == [], "An absent or empty news list must build")
        assert(File.read(File.join(output, "index.html")).include?("No news so far..."),
               "Empty news must have a useful rendered state")
      end
    end

  end

  def expect_error(message, **fixture)
    with_site(**fixture) { raise "Build unexpectedly succeeded; expected #{message.inspect}" }
  rescue Jekyll::Errors::FatalException => error
    assert(error.message.include?(message), "Expected helpful error #{message.inspect}, got #{error.message.inspect}")
  end

  def check_errors
    expect_error("news.yml must contain a list", news: { "date" => "2026-01-15" })
    expect_error("news entry 1 needs a date in YYYY-MM-DD format", news: [entry("Invalid", "2026-02-30")])
    expect_error("news entry 1 needs a date in YYYY-MM-DD format", news: [{ "text" => "Missing date" }])
    expect_error("news entry 1 needs Markdown text", news: [{ "date" => "2026-01-15" }])
    expect_error("news entry 1 needs Markdown text", news: [entry("  ")])
  end

  def render_filter(site, value, filter)
    Liquid::Template.parse("{{ value | #{filter} }}").render!(
      { "value" => value }, registers: { site: site }
    )
  end

  def check_filters
    with_site do |site, _|
      %w[https://example.com/paper http://example.com/paper //cdn.example.com/image.png mailto:hasan@example.com #section relative.pdf].each do |url|
        assert(render_filter(site, url, "site_url") == url, "site_url must preserve #{url.inspect}")
      end
      { "/files/cv.pdf" => "/preview/files/cv.pdf", "/" => "/preview/",
        "/preview/files/cv.pdf" => "/preview/files/cv.pdf", "/preview" => "/preview",
        "/preview?query=1" => "/preview?query=1", "/preview#section" => "/preview#section" }.each do |url, expected|
        assert(render_filter(site, url, "site_url") == expected, "site_url must prefix #{url.inspect} exactly once")
      end
      markdown = '[CV](/files/cv.pdf) and ![Photo](/files/photo.png) and [External](https://example.com/paper)'
      html = render_filter(site, markdown, "site_markdown")
      assert(html.include?('href="/preview/files/cv.pdf"'), "Markdown file links must respect baseurl")
      assert(html.include?('src="/preview/files/photo.png"'), "Markdown image links must respect baseurl")
      assert(html.include?('href="https://example.com/paper"'), "Markdown external links must remain unchanged")
    end

    with_site(baseurl: "") do |site, _|
      assert(render_filter(site, "/files/cv.pdf", "site_url") == "/files/cv.pdf", "Root hosting must preserve root links")
    end

    with_site(news: [entry("Read the [CV](/files/cv.pdf)", "2026-01-15")]) do |_, output|
      assert(File.read(File.join(output, "index.html")).include?('href="/preview/files/cv.pdf"'),
             "News data Markdown must render file links under the preview baseurl")
    end
  end
end

SiteChecks.new.run
