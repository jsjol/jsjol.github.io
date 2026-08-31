# jsjol.github.io

Personal research website for Jens Sjölund, Assistant Professor of Machine
Learning at Uppsala University. Live at <https://jsjol.github.io>.

Built with [Jekyll](https://jekyllrb.com/) on a heavily reduced fork of the
[al-folio](https://github.com/alshedivat/al-folio) theme. Pushing to `master`
triggers the `Deploy site` workflow, which builds the site, purges unused CSS
and publishes `_site` to the `gh-pages` branch.

## Local development

Requires Ruby with Bundler, and ImageMagick for the responsive image variants:

```bash
brew install imagemagick   # provides `magick`
bundle install
bundle exec jekyll serve    # http://localhost:4000
```

The build needs nothing else — no Python, no Node. A clean build takes about
five seconds and should print no warnings; treat any warning as a defect.

Before committing, format the sources:

```bash
npm install                 # first time only
npx prettier . --write
```

## Where the content lives

| What               | Where                                                 |
| ------------------ | ----------------------------------------------------- |
| About page         | `_pages/about.md`                                     |
| News items         | `_news/`                                              |
| Publications       | `_bibliography/papers.bib`                            |
| Research threads   | `_projects/`                                          |
| Courses            | `_teachings/`                                         |
| Group members      | `_data/people.yml`                                    |
| Social links       | `_data/socials.yml`                                   |
| Repository cards   | `_data/repositories.yml`                              |
| CV                 | `assets/pdf/cv.pdf`, linked from `_pages/cv.md`       |
| Scholar paper list | `_data/citations.yml`, feeds new-paper detection only |
| Scholar exclusions | `_data/scholar_ignore.yml`                            |

### Adding a news item

Create `_news/YYYY-MM-DD-slug.md` whose only front matter is its date:

```markdown
---
date: 2026-08-18
---

New paper at [Venue]: [**Title**](link). [One sentence.] Work led by [Author].
```

News items are rendered inline in the news table on `/` and `/news/`, so they
get no standalone pages. Keep the filename date and the front-matter date equal.

### Adding a publication

Append a BibTeX entry to `_bibliography/papers.bib`. Beyond the standard fields,
the templates understand `abbr`, `abstract`, `arxiv`, `award`, `award_name`,
`bibtex_show`, `code`, `html`, `pdf`, `poster`, `preview`, `selected`, `slides`,
`supp`, `video` and `website`. `selected={true}` puts the entry on the front
page; `preview={file.png}` looks for that file in
`assets/img/publication_preview/`.

### Adding an image

Nothing needs to be wider than 1400 px — that is the largest variant
`_includes/figure.liquid` puts in the `srcset`. Compress before committing:

```bash
magick in.png -strip -resize '1400x1400>' -quality 85 out.png
pngquant --quality=70-92 --strip --force --output out.png out.png
```

## Workflows

- **Deploy site** — on every push to `master` that touches site content.
- **Update publications** — Mon/Wed/Fri, in two jobs of deliberately different
  trust levels. See below.

## Keeping the publication list current

`bin/sync_publications.py` diffs the Google Scholar profile against
`_bibliography/papers.bib`. Run it with no arguments for a report:

```bash
python bin/sync_publications.py                    # report only
python bin/sync_publications.py --annotate         # attach Scholar ids
python bin/sync_publications.py --append           # add missing papers
```

**Existing entries are never rewritten.** The bibliography is hand-curated —
`preview` in particular — so the script may only insert a `google_scholar_id`
line into an entry that lacks one, and append new entries at the end of the
file. Both are asserted afterwards: `--append` checks that the previous content
is a byte prefix of the result, and `--annotate` checks that the file grew by
exactly the inserted lines. No field value is ever touched.

The `Update publications` workflow splits this by how much review each half
needs. The `refresh` job attaches Scholar ids and commits straight to `master`
because that is mechanically safe. The `propose` job appends papers that are on
Scholar but not in the bibliography and opens a pull request, because a new entry
needs its venue and author list checked and wants a `preview` and possibly
`selected` added by hand.

### No citation counts are shown

The site used to carry a per-paper Google Scholar count. It does not any more.
Google Scholar answers **every** request from a GitHub runner with HTTP 403 — the
identical request from a home connection returns 200 — so nothing refreshed from
CI after 2026-06-29, and keeping a count on the page meant either showing a stale
number or refreshing by hand three times a week. Switching to a source that
allows CI access was considered and rejected: OpenAlex reports 1356 citations and
h-index 17 against Scholar's 3472 and 25, which is not the same claim.

`_data/citations.yml` is still here, and `bin/update_scholar_citations.py` still
refreshes it:

```bash
conda run -n homepage python bin/update_scholar_citations.py
```

The `homepage` conda env is needed for PyYAML; the interpreter on `PATH` does not
have it. The file's only remaining job is to list the papers Scholar knows about
so `bin/sync_publications.py` can spot ones missing from the bibliography, and
Scholar is better at that than OpenAlex — 106 records against 97. **Nothing on
the site reads it**, so it going stale is not a defect, the workflow attempts the
refresh as best effort, and a failure no longer turns the run red.

Two things worth knowing:

- **Detection costs no Scholar requests.** `bin/update_scholar_citations.py`
  already downloads the whole publication list in one request, so the sync only
  reads `_data/citations.yml`. It never
  calls `scholarly.fill(pub)` per paper, which is what triggers Scholar's
  CAPTCHA and stalls [fetch-publications](https://github.com/jsjol/fetch-publications)
  partway through the list. Metadata for a new paper comes from Crossref, and
  from the arXiv API when Crossref has no record — which is also why the
  generated BibTeX keys carry a real first-author surname rather than `unknown`.
- **Scholar sometimes attributes someone else's paper to the profile.** Add its
  title or publication id to `_data/scholar_ignore.yml` and it will not be
  proposed again. Supervised PhD theses are listed there too: they belong on the
  group page via `_data/people.yml`, not in the publication list.
- **OpenAlex is a second detection source, and is report-only.** It works from CI
  even when Scholar does not, but it keeps separate records for the preprint and
  the published version of the same paper, leaves HTML in titles, and lists
  theses, so its findings are printed for a human to check rather than appended.
  Titles are matched exactly, then on a prefix (for Scholar's truncated titles),
  then on word overlap above 0.72 — which is what recognises "A linear
  programming approach to inverse planning in radiosurgery" as the entry already
  in the file under "… in Gamma Knife radiosurgery".

Where several Scholar records map onto one entry — the patent families all share
titles like "Methods for inverse planning" — the script attaches no id and says
so, rather than guessing which record belongs to which entry.

## Local changes to the theme

This fork has diverged from upstream al-folio deliberately, so updates have to
be cherry-picked rather than merged. The substantive differences:

- The blog, bookshelf, CV-from-JSON, distill, repository-trophy, comment,
  newsletter and search features are removed, along with their layouts,
  includes, Sass partials, data files, assets and CDN libraries.
- MDBootstrap is gone. It cost 277 kB of CSS and 288 kB of JS to supply four
  shadow rules, which now live in `_sass/_utilities.scss`.
- `_plugins/cache-bust.rb` replaces the `jekyll-cache-bust` gem, whose CSS
  digest hashed a directory that does not exist in this repository, so the
  `?v=` query string never changed and browsers served stale CSS.
- An empty `title:` in `_config.yml` names the site after its owner.
  Upstream requires the literal string `blank` for this and renders an empty
  `<h1>` and an empty navbar brand otherwise.
- `_pages/people.md` uses a CSS grid defined in `_sass/_people.scss` rather
  than Bootstrap row/column utilities.
