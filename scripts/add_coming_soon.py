import os
import re

BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "mirror"))
BODY_RE = re.compile(r"(<body\b[^>]*>)", re.IGNORECASE)

OVERLAY = '''<div id="d2g-coming-soon-overlay" style="position:fixed;inset:0;z-index:999999;display:flex;align-items:center;justify-content:center;background:rgba(20,10,5,0.55);padding:20px;">
<div style="background:#ffffff;max-width:480px;width:100%;border-radius:16px;padding:40px 32px;text-align:center;box-shadow:0 20px 60px rgba(0,0,0,0.35);font-family:Arial,Helvetica,sans-serif;">
<div style="width:64px;height:64px;border-radius:14px;background:#C0392B;color:#fff;font-weight:700;font-size:20px;display:flex;align-items:center;justify-content:center;margin:0 auto 20px;">D2G</div>
<h1 style="margin:0 0 10px;font-size:24px;color:#1a1a1a;">We're Cooking Up Something New</h1>
<p style="margin:0 0 6px;font-size:15px;color:#555;line-height:1.5;">D2G Foodstuff trading L.L.C&rsquo;s new website is currently under construction.</p>
<p style="margin:0;font-size:15px;color:#555;line-height:1.5;">Please check back soon &mdash; we&rsquo;ll be live shortly.</p>
</div>
</div>
<style>
html, body { overflow: hidden !important; height: 100% !important; }
body > *:not(#d2g-coming-soon-overlay) { filter: blur(6px); pointer-events: none; user-select: none; }
</style>
'''

MARKER = "d2g-coming-soon-overlay"


def main():
    changed = 0
    total = 0
    for root, _dirs, files in os.walk(BASE):
        for name in files:
            if not name.endswith(".html"):
                continue
            fp = os.path.join(root, name)
            total += 1
            with open(fp, encoding="utf-8") as f:
                content = f.read()
            if MARKER in content:
                continue
            new_content, n = BODY_RE.subn(lambda m: m.group(1) + OVERLAY, content, count=1)
            if n:
                with open(fp, "w", encoding="utf-8") as f:
                    f.write(new_content)
                changed += 1
    print(f"Scanned {total} html files, added overlay to {changed}.")


if __name__ == "__main__":
    main()
