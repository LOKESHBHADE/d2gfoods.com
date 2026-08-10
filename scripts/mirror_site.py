#!/usr/bin/env python3
"""Static mirror of a website: downloads pages + assets, rewrites links to relative local paths."""
import os
import re
import sys
import time
import urllib.parse as up

import requests
from bs4 import BeautifulSoup

START = "https://bombayfoodstuff.com/"
DOMAIN = up.urlparse(START).netloc
OUT_DIR = os.path.join(os.path.dirname(__file__), "..", "mirror")
OUT_DIR = os.path.abspath(OUT_DIR)

PAGE_EXT = (".html", ".htm", "")
ASSET_TAGS = {
    "img": "src",
    "script": "src",
    "link": "href",
    "source": "src",
}

visited_pages = set()
downloaded_assets = set()
queue = [START]

session = requests.Session()
session.headers.update({"User-Agent": "Mozilla/5.0 (compatible; SiteMirror/1.0; owner-authorized)"})


def url_to_local_path(url, is_asset=False):
    parsed = up.urlparse(url)
    path = parsed.path
    if path == "" or path == "/":
        path = "/index.html"
    elif path.endswith("/"):
        path = path + "index.html"
    elif is_asset:
        pass
    else:
        if not os.path.splitext(path)[1]:
            path = path.rstrip("/") + "/index.html"
    local = os.path.join(OUT_DIR, path.lstrip("/"))
    return local


def rel_link(from_path, to_url, is_asset=False):
    to_local = url_to_local_path(to_url, is_asset=is_asset)
    from_dir = os.path.dirname(from_path)
    rel = os.path.relpath(to_local, from_dir)
    return rel.replace(os.sep, "/")


def is_same_domain(url):
    return up.urlparse(url).netloc in ("", DOMAIN)


def fetch(url):
    try:
        r = session.get(url, timeout=20)
        r.raise_for_status()
        return r
    except Exception as e:
        print(f"  FAILED: {url} -> {e}")
        return None


def download_asset(url):
    if url in downloaded_assets:
        return
    if url.startswith("data:") or not is_same_domain(url):
        return
    downloaded_assets.add(url)
    r = fetch(url)
    if r is None:
        return
    local = url_to_local_path(url, is_asset=True)
    os.makedirs(os.path.dirname(local), exist_ok=True)
    with open(local, "wb") as f:
        f.write(r.content)
    print(f"  asset: {url}")


def process_page(url):
    if url in visited_pages:
        return
    visited_pages.add(url)
    r = fetch(url)
    if r is None:
        return
    ctype = r.headers.get("Content-Type", "")
    if "text/html" not in ctype:
        return
    print(f"page: {url}")
    soup = BeautifulSoup(r.text, "html.parser")
    local_path = url_to_local_path(url)

    for tag_name, attr in ASSET_TAGS.items():
        for tag in soup.find_all(tag_name):
            src = tag.get(attr)
            if not src:
                continue
            full = up.urljoin(url, src)
            if not is_same_domain(full):
                continue
            full = full.split("#")[0]
            download_asset(full)
            tag[attr] = rel_link(local_path, full, is_asset=True)

    for tag in soup.find_all("a"):
        href = tag.get("href")
        if not href:
            continue
        full = up.urljoin(url, href)
        full_no_frag = full.split("#")[0]
        if is_same_domain(full_no_frag) and full_no_frag.startswith(START.rstrip("/")):
            clean = full_no_frag.split("?")[0]
            if clean not in visited_pages and clean not in queue:
                queue.append(clean)
            tag["href"] = rel_link(local_path, full_no_frag)

    os.makedirs(os.path.dirname(local_path), exist_ok=True)
    with open(local_path, "w", encoding="utf-8") as f:
        f.write(str(soup))


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    while queue:
        url = queue.pop(0)
        url = url.split("?")[0]
        if url in visited_pages:
            continue
        process_page(url)
        time.sleep(0.3)
    print(f"\nDone. {len(visited_pages)} pages, {len(downloaded_assets)} assets -> {OUT_DIR}")


if __name__ == "__main__":
    main()
