#!/usr/bin/env python
"""Keep _bibliography/papers.bib in step with the Google Scholar profile.

Detection is free: bin/update_scholar_citations.py already downloads the whole
publication list into _data/citations.yml three times a week, so this script only
has to diff that list against the bibliography. Metadata for a newly detected
paper comes from Crossref, which is a stable public API, rather than from a
second Scholar request.

Existing entries are never rewritten. The bibliography carries hand-curated
fields -- `preview` above all, which took real effort to set up -- so the only
two things this script is allowed to do are:

  --annotate  insert a `google_scholar_id` line into an entry that has none,
              which makes future matching exact instead of title-based
  --append    add entries for Scholar records that are not in the bibliography,
              at the end of the file, each marked with a TODO comment

Both are verified after the fact. --append asserts the original file is a byte
prefix of the new one. --annotate asserts the file grew by exactly the inserted
lines, and each insertion is checked against the entry it went into; the only
other change it makes is the comma that the preceding field needs once it is no
longer last. No field value is ever rewritten. Without either flag the script
only reports.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import unicodedata
import urllib.parse
import urllib.request

import yaml

BIB_PATH = "_bibliography/papers.bib"
CITATIONS_PATH = "_data/citations.yml"
SOCIALS_PATH = "_data/socials.yml"
IGNORE_PATH = "_data/scholar_ignore.yml"
CROSSREF = "https://api.crossref.org/works"
# https, not http: the http endpoint 301-redirects and a client that does not
# follow redirects gets an empty body, which looks exactly like "no results".
ARXIV = "https://export.arxiv.org/api/query"
OPENALEX = "https://api.openalex.org"
CONTACT = "jens.sjolund@it.uu.se"  # Crossref asks callers to identify themselves


# --------------------------------------------------------------------------- #
# Bibliography parsing. Entries are kept as raw text so that anything this
# script does not understand survives untouched.
# --------------------------------------------------------------------------- #


class Entry:
    def __init__(self, text: str):
        self.text = text
        m = re.match(r"@(\w+)\s*\{\s*([^,\s]+)\s*,", text)
        self.type = m.group(1) if m else ""
        self.key = m.group(2) if m else ""
        self.title = self._field("title")
        self.scholar_id = self._field("google_scholar_id")

    def _field(self, name: str) -> str:
        m = re.search(
            r"^\s*" + name + r"\s*=\s*\{(.*?)\}\s*,?\s*$",
            self.text,
            re.MULTILINE | re.DOTALL,
        )
        if not m:
            return ""
        return re.sub(r"[{}]", "", m.group(1)).strip()


def parse_bib(text: str) -> list[Entry]:
    # Entries start at column 0 with @, which is true throughout this file.
    starts = [m.start() for m in re.finditer(r"^@", text, re.MULTILINE)]
    entries = []
    for i, start in enumerate(starts):
        end = starts[i + 1] if i + 1 < len(starts) else len(text)
        entries.append(Entry(text[start:end]))
    return entries


def normalize(title: str) -> str:
    """A title reduced to something comparable across Scholar and BibTeX."""
    title = re.sub(r"<[^>]+>", "", title)  # OpenAlex leaves markup in titles
    t = unicodedata.normalize("NFKD", title)
    t = "".join(c for c in t if not unicodedata.combining(c))
    t = t.replace("‐", "-").replace("–", "-").replace("—", "-")
    return re.sub(r"[^a-z0-9]+", " ", t.lower()).strip()


def squash(title: str) -> str:
    """Normalized and with spaces removed, for comparing truncated titles.

    Scholar cuts long titles off and occasionally loses a space ("forOptimization"),
    so an exact comparison misses entries that are in fact already present.
    """
    return normalize(title).replace(" ", "")


_prefix_matches: list[tuple[str, str]] = []
_fuzzy_matches: list[tuple[str, str, float]] = []

SQUASH_PREFIX_MIN = 30  # below this length a prefix agreement is not evidence


def token_overlap(a: str, b: str) -> float:
    """Jaccard overlap of the word sets of two normalized titles."""
    sa, sb = set(normalize(a).split()), set(normalize(b).split())
    if not sa or not sb:
        return 0.0
    return len(sa & sb) / len(sa | sb)


TOKEN_OVERLAP_MIN = 0.72  # below this, two titles are different papers


def find_by_title(title: str, entries: list["Entry"], exact: dict) -> "Entry | None":
    """Match on the normalized title, falling back to a guarded prefix match.

    Exact agreement is tried first and at any length, because several of the
    patents have titles as short as "Treatment planning". The prefix fallback
    exists only for Scholar's truncated titles, so it requires both sides to be
    long enough that agreeing on a prefix means something.
    """
    key = normalize(title)
    if key in exact:
        return exact[key]

    target = squash(title)
    global _prefix_matches, _fuzzy_matches
    if len(target) < SQUASH_PREFIX_MIN:
        return None
    for e in entries:
        candidate = squash(e.title)
        if len(candidate) < SQUASH_PREFIX_MIN:
            continue
        if candidate.startswith(target) or target.startswith(candidate):
            _prefix_matches.append((title, e.key))
            return e

    # Last resort: the same paper worded differently by two sources.
    best, best_score = None, 0.0
    for e in entries:
        score = token_overlap(title, e.title)
        if score > best_score:
            best, best_score = e, score
    if best is not None and best_score >= TOKEN_OVERLAP_MIN:
        _fuzzy_matches.append((title, best.key, best_score))
        return best
    return None


# --------------------------------------------------------------------------- #
# Crossref lookup
# --------------------------------------------------------------------------- #


def openalex_works(orcid: str) -> list[dict]:
    """Every work OpenAlex attributes to `orcid`, deduplicated by title.

    A second detection source matters because Google Scholar refuses requests
    from CI runners, so _data/citations.yml can be weeks stale. OpenAlex has a
    real API with no such restriction. It does keep two records for most arXiv
    items, one with a DOI and one without, hence the deduplication.
    """
    try:
        url = f"{OPENALEX}/authors?filter=orcid:{orcid}&mailto={CONTACT}"
        with urllib.request.urlopen(url, timeout=30) as r:
            authors = json.load(r)["results"]
        if not authors:
            print("    OpenAlex knows no author with that ORCID")
            return []
        author_id = authors[0]["id"].rsplit("/", 1)[-1]

        works, page = [], 1
        while True:
            url = (
                f"{OPENALEX}/works?filter=author.id:{author_id}&per-page=200&page={page}"
                f"&select=doi,title,publication_year,type&mailto={CONTACT}"
            )
            with urllib.request.urlopen(url, timeout=30) as r:
                payload = json.load(r)
            works.extend(payload["results"])
            if len(works) >= payload["meta"]["count"] or not payload["results"]:
                break
            page += 1
    except Exception as e:  # noqa: BLE001
        print(f"    OpenAlex lookup failed: {e}")
        return []

    seen, unique = set(), []
    for w in works:
        title = (w.get("title") or "").strip()
        key = squash(title)
        if not key or key in seen:
            continue
        seen.add(key)
        unique.append(w)
    return unique


def crossref_lookup(title: str) -> dict | None:
    """Return Crossref metadata for `title`, or None if nothing matches it."""
    query = urllib.parse.urlencode(
        {
            "query.bibliographic": title,
            "rows": 3,
            "select": "DOI,title,container-title,issued,type,author,volume,issue,page,publisher",
            "mailto": CONTACT,
        }
    )
    try:
        with urllib.request.urlopen(f"{CROSSREF}?{query}", timeout=30) as r:
            items = json.load(r)["message"]["items"]
    except Exception as e:  # noqa: BLE001 - a lookup failure must not stop the sync
        print(f"    Crossref lookup failed: {e}")
        return None

    target = normalize(title)
    for item in items:
        candidate = (item.get("title") or [""])[0]
        if normalize(candidate) == target:
            return item
    return None


def arxiv_lookup(title: str) -> dict | None:
    """Return arXiv metadata for `title`, or None. Covers the ML preprints and
    conference papers that Crossref never sees."""
    query = urllib.parse.urlencode(
        {"search_query": f'ti:"{title}"', "max_results": 5, "start": 0}
    )
    try:
        with urllib.request.urlopen(f"{ARXIV}?{query}", timeout=30) as r:
            feed = r.read().decode("utf-8", "replace")
    except Exception as e:  # noqa: BLE001
        print(f"    arXiv lookup failed: {e}")
        return None

    target = squash(title)
    for m in re.finditer(r"<entry>(.*?)</entry>", feed, re.S):
        e = m.group(1)
        got = re.search(r"<title>(.*?)</title>", e, re.S)
        ident = re.search(r"<id>https?://arxiv\.org/abs/([^<]+)</id>", e)
        if not (got and ident):
            continue
        clean = re.sub(r"\s+", " ", got.group(1)).strip()
        candidate = squash(clean)
        if not (candidate == target or candidate.startswith(target) or target.startswith(candidate)):
            continue
        published = re.search(r"<published>(\d{4})", e)
        summary = re.search(r"<summary>(.*?)</summary>", e, re.S)
        return {
            "arxiv_id": re.sub(r"v\d+$", "", ident.group(1)),
            "title": clean,
            "authors": [a.strip() for a in re.findall(r"<name>(.*?)</name>", e)],
            "year": published.group(1) if published else "",
            "abstract": re.sub(r"\s+", " ", summary.group(1)).strip() if summary else "",
        }
    return None


def bib_from_arxiv(rec: dict, scholar_id: str, title: str, year: str) -> str:
    fields = [
        ("title", "{" + title + "}"),
        ("author", " and ".join(rec["authors"]) or "TODO"),
        ("year", rec["year"] or year),
        ("journal", "arXiv preprint arXiv:" + rec["arxiv_id"]),
    ]
    if rec.get("abstract"):
        fields.append(("abstract", rec["abstract"]))
    fields += [
        ("url", "https://arxiv.org/abs/" + rec["arxiv_id"]),
        ("eprint", rec["arxiv_id"]),
        ("archiveprefix", "arXiv"),
    ]
    if scholar_id:
        fields.append(("google_scholar_id", scholar_id))
    key = make_key(rec["authors"], rec["year"] or year, title)
    width = max(len(n) for n, _ in fields)
    body = "\n".join(f"  {n.ljust(width)} = {{{v}}}," for n, v in fields)
    return (
        f"% TODO from arXiv: check whether this has since appeared at a venue, then\n"
        f"%   add abbr, preview and selected as appropriate.\n"
        f"@article{{{key},\n{body.rstrip(',')}\n}}\n"
    )


def bib_from_crossref(item: dict, scholar_id: str, title: str, year: str) -> str:
    authors = []
    for a in item.get("author", []) or []:
        given, family = a.get("given", "").strip(), a.get("family", "").strip()
        authors.append(f"{given} {family}".strip())
    venue = (item.get("container-title") or [""])[0]
    issued = (item.get("issued", {}).get("date-parts") or [[None]])[0]
    crossref_year = str(issued[0]) if issued and issued[0] else year
    is_proceedings = item.get("type") in ("proceedings-article", "book-chapter")

    fields = [("title", "{" + title + "}"), ("author", " and ".join(authors) or "TODO")]
    fields.append(("year", crossref_year))
    fields.append(("booktitle" if is_proceedings else "journal", venue or "TODO"))
    for name, key in (("volume", "volume"), ("number", "issue"), ("pages", "page")):
        if item.get(key):
            fields.append((name, str(item[key])))
    if item.get("publisher"):
        fields.append(("publisher", item["publisher"]))
    if item.get("DOI"):
        fields.append(("doi", item["DOI"]))
        fields.append(("url", "https://doi.org/" + item["DOI"]))
    if scholar_id:
        fields.append(("google_scholar_id", scholar_id))

    key = make_key(authors, crossref_year, title)
    width = max(len(n) for n, _ in fields)
    body = "\n".join(f"  {n.ljust(width)} = {{{v}}}," for n, v in fields)
    kind = "inproceedings" if is_proceedings else "article"
    return (
        f"% TODO review this entry: check the venue and author list, then add\n"
        f"%   abbr, abstract, preview and selected as appropriate.\n"
        f"@{kind}{{{key},\n{body.rstrip(',')}\n}}\n"
    )


def bib_stub(scholar_id: str, title: str, year: str) -> str:
    """A minimal entry for a paper Crossref does not know, e.g. a PMLR paper."""
    key = make_key([], year, title)
    fields = [
        ("title", "{" + title + "}"),
        ("author", "TODO"),
        ("year", year),
        ("journal", "TODO"),
    ]
    if scholar_id:
        fields.append(("google_scholar_id", scholar_id))
    width = max(len(n) for n, _ in fields)
    body = "\n".join(f"  {n.ljust(width)} = {{{v}}}," for n, v in fields)
    return (
        f"% TODO Crossref had no record for this one, so only the title, year and\n"
        f"%   Scholar id are filled in. Complete the author list and venue, then add\n"
        f"%   abbr, abstract, preview and selected as appropriate.\n"
        f"@article{{{key},\n{body.rstrip(',')}\n}}\n"
    )


def make_key(authors: list[str], year: str, title: str) -> str:
    surname = authors[0].split()[-1].lower() if authors else "unknown"
    surname = re.sub(r"[^a-z]", "", normalize(surname)) or "unknown"
    first_word = next((w for w in normalize(title).split() if len(w) > 3), "paper")
    return f"{surname}{year}{first_word}"


# --------------------------------------------------------------------------- #


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--annotate",
        action="store_true",
        help="add google_scholar_id to matched entries that lack it",
    )
    ap.add_argument(
        "--append",
        action="store_true",
        help="append entries for Scholar records missing from the bibliography",
    )
    args = ap.parse_args()

    scholar_userid = yaml.safe_load(open(SOCIALS_PATH))["scholar_userid"]
    citations = yaml.safe_load(open(CITATIONS_PATH)) or {}
    papers = citations.get("papers") or {}
    if not papers:
        print(f"{CITATIONS_PATH} lists no papers; run update_scholar_citations.py first.")
        return 1

    try:
        ignore_raw = yaml.safe_load(open(IGNORE_PATH)) or {}
    except FileNotFoundError:
        ignore_raw = {}
    ignored_ids = set(ignore_raw.get("publication_ids") or [])
    ignored_titles = {squash(t) for t in (ignore_raw.get("titles") or [])}

    original = open(BIB_PATH, encoding="utf-8").read()
    entries = parse_bib(original)
    print(f"{len(entries)} entries in {BIB_PATH}, {len(papers)} records on Scholar\n")

    by_scholar_id = {e.scholar_id: e for e in entries if e.scholar_id}
    by_title_exact: dict[str, Entry] = {}
    for e in entries:
        if e.title:
            by_title_exact.setdefault(normalize(e.title), e)
    matched, unmatched, ignored, openalex_only = {}, [], [], []
    claims: dict[str, list] = {}
    for full_key, rec in papers.items():
        # citations.yml keys are "<scholar_userid>:<publication id>".
        pub_id = full_key.split(":", 1)[1] if ":" in full_key else full_key
        title = str(rec.get("title", "")).strip()
        year = str(rec.get("year", "")).strip()

        if pub_id in ignored_ids or squash(title) in ignored_titles:
            ignored.append((pub_id, title))
            continue

        entry = by_scholar_id.get(pub_id) or find_by_title(title, entries, by_title_exact)
        if entry is None:
            unmatched.append((pub_id, title, year))
            continue
        matched[pub_id] = entry
        claims.setdefault(entry.key, []).append((entry, pub_id, title))

    ambiguous = []
    to_annotate = []
    for key, claimed in claims.items():
        entry = claimed[0][0]
        if entry.scholar_id:
            continue
        if len(claimed) == 1:
            to_annotate.append((entry, claimed[0][1]))
        else:
            ambiguous.append((key, [t for _, _, t in claimed]))

    # Second detection pass: OpenAlex, which CI can always reach.
    orcid = yaml.safe_load(open(SOCIALS_PATH)).get("orcid_id")
    if orcid:
        print("\nChecking OpenAlex as well...")
        seen_unmatched = {squash(t) for _, t, _ in unmatched}
        for w in openalex_works(orcid):
            title = (w.get("title") or "").strip()
            year = str(w.get("publication_year") or "")
            key = squash(title)
            if key in seen_unmatched:
                continue
            if key in ignored_titles or not title:
                ignored.append(("", title))
                continue
            if find_by_title(title, entries, by_title_exact) is not None:
                continue
            seen_unmatched.add(key)
            openalex_only.append((title, year))

    bib_only = [e for e in entries if e not in matched.values()]

    print(f"matched:                 {len(matched)}")
    print(f"missing a scholar id:    {len(to_annotate)}")
    print(f"on Scholar, not in bib:  {len(unmatched)}")
    print(f"in bib, not on Scholar:  {len(bib_only)}")
    print(f"ignored by {IGNORE_PATH}: {len(ignored)}")
    print(f"ambiguous, left alone:    {len(ambiguous)}")

    if _prefix_matches:
        print("\nMatched on a truncated Scholar title (worth an eye):")
        for scholar_title, key in _prefix_matches:
            print(f"  {key}  <-  {scholar_title[:66]}")
    if ambiguous:
        print("\nSeveral Scholar records share one entry, so no id was attached:")
        for key, titles in ambiguous:
            print(f"  {key}: {len(titles)}x {titles[0][:56]}")

    if unmatched:
        print("\nOn Scholar but not in the bibliography:")
        for pub_id, title, year in unmatched:
            print(f"  {year}  {title[:78]}")
    if _fuzzy_matches:
        print("\nMatched on word overlap rather than an exact title (worth an eye):")
        for src_title, key, score in _fuzzy_matches:
            print(f"  {key}  <-  {score:.2f}  {src_title[:58]}")
    if openalex_only:
        print("\nOn OpenAlex but not in the bibliography. NOT appended, because")
        print("OpenAlex keeps separate records for preprint and published versions")
        print("and also lists theses; check these by hand:")
        for title, year in openalex_only:
            print(f"  {year}  {title[:74]}")
    if bib_only:
        print("\nIn the bibliography but not on Scholar (left alone):")
        for e in bib_only:
            print(f"  {e.key}: {e.title[:70]}")

    if not (args.annotate or args.append):
        print("\nReport only. Pass --annotate and/or --append to write.")
        return 0

    text = original

    if args.annotate and to_annotate:
        inserted_bytes = 0
        for entry, pub_id in to_annotate:
            # Insert immediately before the entry's closing brace, matching the
            # alignment of the field above it.
            m = re.search(r"\n\}\s*$", entry.text)
            assert m, f"could not find the end of entry {entry.key}"
            indent_match = re.search(r"^(\s*)(\S+)(\s*)=", entry.text, re.MULTILINE)
            pad = len(indent_match.group(2)) + len(indent_match.group(3))
            name = "google_scholar_id".ljust(max(pad, len("google_scholar_id")))
            before = entry.text[: m.start()]
            line = f",\n  {name} = {{{pub_id}}}"
            new_entry = before.rstrip().rstrip(",") + line + entry.text[m.start() :]
            # The only difference must be the inserted line.
            assert new_entry.replace(line, "", 1) == before.rstrip().rstrip(",") + entry.text[m.start() :], (
                f"insertion perturbed entry {entry.key}"
            )
            inserted_bytes += len(new_entry) - len(entry.text)
            assert entry.text in text, f"entry {entry.key} not found verbatim"
            text = text.replace(entry.text, new_entry, 1)
        print(f"\nAnnotated {len(to_annotate)} entries with their Scholar id.")

        # Verify: the file must have grown by exactly the inserted lines, and
        # nothing else may differ.
        assert len(text) == len(original) + inserted_bytes, (
            "annotation changed more than the inserted lines; refusing to write"
        )

    if args.append and unmatched:
        # The prefix check below must be against the text as it stands now, which
        # annotation may already have changed.
        text_before_append = text
        additions = []
        for pub_id, title, year in unmatched:
            print(f"\n  building an entry for: {title[:70]}")
            item = crossref_lookup(title)
            if item:
                print(f"    Crossref: {item.get('DOI')}")
                additions.append(bib_from_crossref(item, pub_id, title, year))
                continue
            rec = arxiv_lookup(title)
            if rec:
                print(f"    arXiv: {rec['arxiv_id']}")
                additions.append(bib_from_arxiv(rec, pub_id, title, year))
                continue
            print("    neither Crossref nor arXiv had a record; writing a stub")
            additions.append(bib_stub(pub_id, title, year))
        text = text.rstrip("\n") + "\n\n" + "\n".join(additions)
        print(f"\nAppended {len(additions)} entries.")

    if text == original:
        print("\nNothing to change.")
        return 0

    if args.append and unmatched:
        assert text.startswith(text_before_append.rstrip("\n")), (
            "append mode altered existing content; refusing to write"
        )

    open(BIB_PATH, "w", encoding="utf-8").write(text)
    print(f"\nWrote {BIB_PATH}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
