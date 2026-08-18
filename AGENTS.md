# Agent guidelines

See [README.md](README.md) for what this repository is, how to build it, where
the content lives, and how this fork differs from upstream al-folio.

Two rules that are easy to get wrong here:

- **Run a clean build and read its output.** `rm -rf .jekyll-cache _site &&
bundle exec jekyll build` should finish in a few seconds with no warnings.
  A warning is a defect, not noise.
- **Look at the page.** Every rendering defect found in this repository so far
  was found by looking at a rendered page, and none by reading the source: an
  empty `<h1>`, missing grid gutters, an unclosed anchor, an empty `href`.
  Serve `_site` and open the page you changed.

Run `npx prettier . --write` before committing.
