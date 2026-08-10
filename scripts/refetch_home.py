import os
import sys
import urllib.parse as up

import requests
from bs4 import BeautifulSoup

START = "https://bombayfoodstuff.com/"
DOMAIN = up.urlparse(START).netloc
OUT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "mirror"))

ASSET_TAGS = {"img": "src", "script": "src", "link": "href", "source": "src"}

session = requests.Session()
session.headers.update({"User-Agent": "Mozilla/5.0 (compatible; SiteMirror/1.0; owner-authorized)"})


def url_to_local_path(url, is_asset=False):
    parsed = up.urlparse(url)
    path = parsed.path
    if path in ("", "/"):
        path = "/index.html"
    elif path.endswith("/"):
        path = path + "index.html"
    elif not is_asset and not os.path.splitext(path)[1]:
        path = path.rstrip("/") + "/index.html"
    return os.path.join(OUT_DIR, path.lstrip("/"))


def rel_link(from_path, to_url, is_asset=False):
    to_local = url_to_local_path(to_url, is_asset=is_asset)
    rel = os.path.relpath(to_local, os.path.dirname(from_path))
    return rel.replace(os.sep, "/")


def is_same_domain(url):
    return up.urlparse(url).netloc in ("", DOMAIN)


r = session.get(START, timeout=30, allow_redirects=True)
r.raise_for_status()
print("Final URL after redirects:", r.url)
print("Status:", r.status_code)

soup = BeautifulSoup(r.text, "html.parser")
print("Title:", soup.title.string if soup.title else None)

local_path = url_to_local_path(START)

for tag_name, attr in ASSET_TAGS.items():
    for tag in soup.find_all(tag_name):
        src = tag.get(attr)
        if not src:
            continue
        full = up.urljoin(START, src)
        if not is_same_domain(full):
            continue
        full = full.split("#")[0]
        tag[attr] = rel_link(local_path, full, is_asset=True)

for tag in soup.find_all("a"):
    href = tag.get("href")
    if not href:
        continue
    full = up.urljoin(START, href).split("#")[0]
    if is_same_domain(full) and full.startswith(START.rstrip("/")):
        tag["href"] = rel_link(local_path, full)

os.makedirs(os.path.dirname(local_path), exist_ok=True)
with open(local_path, "w", encoding="utf-8") as f:
    f.write(str(soup))
print("Wrote:", local_path)
