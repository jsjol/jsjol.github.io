# Appends a ?v=<md5> query string to local asset URLs so that a changed asset is
# refetched and an unchanged one stays cached.
#
# This replaces the jekyll-cache-bust gem, whose bust_css_cache digested the
# directory "assets/_sass" — a path that does not exist in this repository. The
# digest of an empty file list is MD5("") = d41d8cd98f00b204e9800998ecf8427e, so
# the query string never changed and browsers kept serving stale CSS after a
# deploy.
#
#   bust_file_cache — for a file that exists in the source tree as served.
#   bust_css_cache  — for /assets/css/main.css, which does not exist until Sass
#                     runs, so the digest is taken over the Sass sources instead.
module Jekyll
  module CacheBust
    require "digest/md5"

    SASS_SOURCES = ["_sass/**/*", "assets/css/main.scss"].freeze

    def bust_file_cache(url)
      source = url.sub(%r{\A.*?(?=assets/)}, "").sub(/\?.*\z/, "")
      return url unless File.file?(source)

      "#{url}?v=#{Digest::MD5.file(source).hexdigest}"
    end

    def bust_css_cache(url)
      digest = Digest::MD5.new
      SASS_SOURCES.flat_map { |pattern| Dir.glob(pattern) }
                  .select { |path| File.file?(path) }
                  .sort
                  .each { |path| digest << path << Digest::MD5.file(path).digest }
      "#{url}?v=#{digest.hexdigest}"
    end
  end
end

Liquid::Template.register_filter(Jekyll::CacheBust)
