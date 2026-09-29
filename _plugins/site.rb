# frozen_string_literal: true

require "date"

# Custom build code: content URLs, stable news ordering, and a favicon fallback.
module PersonalSite
  # Some browsers request favicon.ico before inspecting the page's icon links.
  # Generate it from the configured ICO so there is only one source to maintain.
  class FaviconFile < Jekyll::StaticFile
    def destination(dest)
      File.join(dest, "favicon.ico")
    end
  end

  class FaviconGenerator < Jekyll::Generator
    def generate(site)
      path = site.config["icon_fallback"].to_s
      return if path.empty?

      relative = path.delete_prefix("/")
      site.static_files << FaviconFile.new(site, site.source, File.dirname(relative), File.basename(relative))
    end
  end

  module Filters
    # Internal links also work when this site is hosted under a project subpath.
    def site_url(input)
      url = input.to_s
      return url unless url.start_with?("/") && !url.start_with?("//")

      base = @context.registers[:site].baseurl.to_s.chomp("/")
      return url if !base.empty? && (url == base || url.start_with?("#{base}/", "#{base}?", "#{base}#"))

      relative_url(url)
    end

    # Markdown in data files can use ordinary /files/... links, too.
    def local_links(html)
      html.to_s.gsub(/(\b(?:href|src)\s*=\s*)(["'])(\/(?!\/)[^"']*)\2/) do
        "#{Regexp.last_match(1)}#{Regexp.last_match(2)}#{site_url(Regexp.last_match(3))}#{Regexp.last_match(2)}"
      end
    end

    def site_markdown(input)
      local_links(markdownify(input))
    end
  end

  class ContentGenerator < Jekyll::Generator
    priority :high

    def generate(site)
      news = site.data.fetch("news", [])
      fail_build("news.yml must contain a list") unless news.is_a?(Array)
      sorted = news.each_with_index.map do |item, index|
        unless item.is_a?(Hash) && item["text"].is_a?(String) && !item["text"].strip.empty?
          fail_build("news entry #{index + 1} needs Markdown text")
        end
        begin
          value = item.fetch("date").to_s
          raise Date::Error unless value.match?(/\A\d{4}-\d{2}-\d{2}\z/)
          date = Date.iso8601(value)
        rescue KeyError, Date::Error
          fail_build("news entry #{index + 1} needs a date in YYYY-MM-DD format")
        end
        [-date.jd, index, item]
      end
      site.data["news"] = sorted.sort_by { |date, index, _| [date, index] }.map(&:last)
    end

    private

    def fail_build(message)
      raise Jekyll::Errors::FatalException, message
    end
  end
end

Liquid::Template.register_filter(PersonalSite::Filters)
