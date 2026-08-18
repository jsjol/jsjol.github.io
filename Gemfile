source 'https://rubygems.org'

gem 'jekyll'

group :jekyll_plugins do
  gem 'jekyll-3rd-party-libraries' # resolves the CDN URLs in _config.yml
  gem 'jekyll-email-protect'       # obfuscates the email address in the social links
  gem 'jekyll-feed'                # /feed.xml
  gem 'jekyll-imagemagick'         # responsive WebP variants; needs imagemagick on PATH
  gem 'jekyll-link-attributes'     # rel/target on external links
  gem 'jekyll-minifier'            # HTML whitespace handling
  gem 'jekyll-regex-replace'       # used by _layouts/bib.liquid
  gem 'jekyll-scholar'             # BibTeX -> publication list
  gem 'jekyll-sitemap'             # /sitemap.xml
  gem 'jekyll-socials'             # {% social_links %}
end

group :other_plugins do
  gem 'css_parser' # used by jekyll-minifier
  gem 'observer'   # used by jekyll-scholar
end
