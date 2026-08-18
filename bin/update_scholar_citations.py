#!/usr/bin/env python
"""Refresh _data/citations.yml from the Google Scholar profile.

Two paths. The primary one is a single GET of the profile page, parsed for the
publication table: it yields the title, year, citation count and publication id
for every paper in one or two requests. The fallback is `scholarly`, which is
what this script used to do exclusively -- but scholarly issues several requests
and Google answers datacenter addresses with a CAPTCHA, which is why the
scheduled workflow produced nothing for seven weeks while reporting success.

Neither path is guaranteed to work from CI. The workflow warns on failure and
turns red once this file is more than ten days old; running this script locally
takes about ten seconds.
"""

import os
import re
import sys
import urllib.request
from datetime import datetime

import yaml


def load_scholar_user_id() -> str:
    """Load the Google Scholar user ID from the configuration file."""
    config_file = "_data/socials.yml"
    if not os.path.exists(config_file):
        print(
            f"Configuration file {config_file} not found. Please ensure the file exists and contains your Google Scholar user ID."
        )
        sys.exit(1)
    try:
        with open(config_file, "r") as f:
            config = yaml.safe_load(f)
        scholar_user_id = config.get("scholar_userid")
        if not scholar_user_id:
            print(
                "No 'scholar_userid' found in the configuration file. Please add 'scholar_userid' to _data/socials.yml."
            )
            sys.exit(1)
        return scholar_user_id
    except yaml.YAMLError as e:
        print(
            f"Error parsing YAML file {config_file}: {e}. Please check the file for correct YAML syntax."
        )
        sys.exit(1)


SCHOLAR_USER_ID: str = load_scholar_user_id()
OUTPUT_FILE: str = "_data/citations.yml"
PROFILE_URL = "https://scholar.google.com/citations"
# Google serves the profile page differently to an unrecognised client.
USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/120.0 Safari/537.36"
)
PAGE_SIZE = 100


def fetch_from_profile_page(user_id: str) -> dict:
    """Parse the publication table straight off the profile page.

    Returns {"<user_id>:<pub_id>": {title, year, citations}} or {} on failure,
    keeping the same shape the scholarly path produces.
    """
    papers: dict = {}
    for start in range(0, 1000, PAGE_SIZE):
        url = f"{PROFILE_URL}?user={user_id}&hl=en&cstart={start}&pagesize={PAGE_SIZE}"
        try:
            request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
            with urllib.request.urlopen(request, timeout=30) as response:
                html = response.read().decode("utf-8", "replace")
        except Exception as e:  # noqa: BLE001
            print(f"Profile page request failed at offset {start}: {e}")
            return {}

        rows = re.findall(r'<tr class="gsc_a_tr">(.*?)</tr>', html, re.S)
        if not rows:
            break

        for row in rows:
            ident = re.search(r"citation_for_view=([\w-]+:[\w-]+)", row)
            title = re.search(r'class="gsc_a_at"[^>]*>(.*?)</a>', row, re.S)
            cites = re.search(r'class="gsc_a_ac[^"]*"[^>]*>([\d,]*)<', row)
            year = re.search(r'class="gsc_a_h[^"]*"[^>]*>(\d*)<', row)
            if not (ident and title):
                continue
            clean = re.sub(r"<[^>]+>", "", title.group(1)).strip()
            count = (cites.group(1) if cites else "").replace(",", "")
            papers[ident.group(1)] = {
                "title": clean,
                "year": (year.group(1) if year else "") or "Unknown Year",
                "citations": int(count) if count else 0,
            }

        if len(rows) < PAGE_SIZE:
            break

    print(f"Profile page gave {len(papers)} publications.")
    return papers


def get_scholar_citations() -> None:
    """Fetch and update Google Scholar citation data."""
    print(f"Fetching citations for Google Scholar ID: {SCHOLAR_USER_ID}")
    today = datetime.now().strftime("%Y-%m-%d")

    # Check if the output file was already updated today
    if os.path.exists(OUTPUT_FILE):
        try:
            with open(OUTPUT_FILE, "r") as f:
                existing_data = yaml.safe_load(f)
            if (
                existing_data
                and "metadata" in existing_data
                and "last_updated" in existing_data["metadata"]
            ):
                print(f"Last updated on: {existing_data['metadata']['last_updated']}")
                if existing_data["metadata"]["last_updated"] == today:
                    print("Citations data is already up-to-date. Skipping fetch.")
                    return
        except Exception as e:
            print(
                f"Warning: Could not read existing citation data from {OUTPUT_FILE}: {e}. The file may be missing or corrupted."
            )

    citation_data = {"metadata": {"last_updated": today}, "papers": {}}

    papers = fetch_from_profile_page(SCHOLAR_USER_ID)
    if papers:
        citation_data["papers"] = papers
    else:
        print("Falling back to scholarly.")
        citation_data["papers"] = fetch_via_scholarly()

    if not citation_data["papers"]:
        print("Both paths failed; leaving the existing data in place.")
        sys.exit(1)

    # Write even when no count moved. metadata.last_updated has to mean "last
    # successful fetch", because that is what the workflow's staleness check
    # reads: if the date only advanced when a number changed, a quiet ten days
    # would look identical to Google refusing every request.
    if existing_data and existing_data.get("papers") == citation_data["papers"]:
        print("No count changed; recording the successful fetch anyway.")

    try:
        with open(OUTPUT_FILE, "w") as f:
            yaml.dump(citation_data, f, width=1000, sort_keys=True)
        print(f"Citation data saved to {OUTPUT_FILE}")
    except Exception as e:
        print(
            f"Error writing citation data to {OUTPUT_FILE}: {e}. Please check file permissions and disk space."
        )
        sys.exit(1)


def fetch_via_scholarly() -> dict:
    """The original path, kept as a fallback. scholarly is optional."""
    try:
        from scholarly import scholarly
    except ImportError:
        print("scholarly is not installed; skipping the fallback.")
        return {}

    papers: dict = {}
    scholarly.set_timeout(15)
    scholarly.set_retries(3)
    try:
        author = scholarly.search_author_id(SCHOLAR_USER_ID)
        author_data = scholarly.fill(author)
    except Exception as e:
        print(f"scholarly failed for user ID '{SCHOLAR_USER_ID}': {e}")
        return {}

    if not author_data or "publications" not in author_data:
        print(f"scholarly returned no publications for user ID '{SCHOLAR_USER_ID}'.")
        return {}

    for pub in author_data["publications"]:
        try:
            pub_id = pub.get("pub_id") or pub.get("author_pub_id")
            if not pub_id:
                print(
                    f"Warning: No ID found for publication: {pub.get('bib', {}).get('title', 'Unknown')}. This publication will be skipped."
                )
                continue

            title = pub.get("bib", {}).get("title", "Unknown Title")
            year = pub.get("bib", {}).get("pub_year", "Unknown Year")
            citations = pub.get("num_citations", 0)

            print(f"Found: {title} ({year}) - Citations: {citations}")

            papers[pub_id] = {
                "title": title,
                "year": year,
                "citations": citations,
            }
        except Exception as e:
            print(
                f"Error processing publication '{pub.get('bib', {}).get('title', 'Unknown')}': {e}. This publication will be skipped."
            )

    return papers


if __name__ == "__main__":
    try:
        get_scholar_citations()
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)
