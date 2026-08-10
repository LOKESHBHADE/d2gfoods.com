import os
import re
import time

import requests

BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "mirror"))
LIVE = "https://bombayfoodstuff.com"
PATTERN = re.compile(r'(?<![\w./-])(/wp-content/uploads/[^\s"\'(),]+)')

session = requests.Session()
session.headers.update({"User-Agent": "Mozilla/5.0 (compatible; SiteMirror/1.0; owner-authorized)"})

missing = set()
for root, _dirs, files in os.walk(BASE):
    for name in files:
        if not name.endswith(".html"):
            continue
        fp = os.path.join(root, name)
        with open(fp, encoding="utf-8", errors="ignore") as f:
            content = f.read()
        for m in PATTERN.finditer(content):
            path = m.group(1)
            if "*" in path:
                continue
            local = os.path.join(BASE, path.lstrip("/"))
            if not os.path.isfile(local):
                missing.add(path)

print(f"Fetching {len(missing)} missing files...")
ok = fail = 0
for path in sorted(missing):
    url = LIVE + path
    local = os.path.join(BASE, path.lstrip("/"))
    try:
        r = session.get(url, timeout=20)
        if r.status_code == 200:
            os.makedirs(os.path.dirname(local), exist_ok=True)
            with open(local, "wb") as f:
                f.write(r.content)
            ok += 1
        else:
            print(f"  {r.status_code}: {path}")
            fail += 1
    except Exception as e:
        print(f"  ERROR {path}: {e}")
        fail += 1
    time.sleep(0.05)

print(f"Done. ok={ok} fail={fail}")
