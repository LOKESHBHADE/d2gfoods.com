import os
import re

BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "mirror"))

DIV_TAG_RE = re.compile(r"<div\b|</div>")


def remove_balanced_div(content, marker):
    idx = content.find(marker)
    if idx == -1:
        return content, False
    start = content.rfind("<div", 0, idx)
    if start == -1:
        return content, False
    depth = 0
    end = None
    for m in DIV_TAG_RE.finditer(content, start):
        if m.group() == "<div":
            depth += 1
        else:
            depth -= 1
            if depth == 0:
                end = m.end()
                break
    if end is None:
        return content, False
    return content[:start] + content[end:], True


# file -> (apex card marker, as-impex card marker)
TARGETS = {
    os.path.join(BASE, "index.html"): (
        "elementor-element-3a74b56",
        "elementor-element-b80ddc2",
    ),
    os.path.join(BASE, "about-us", "index.html"): (
        "elementor-element-1ff51ab",
        "elementor-element-3f0b8cff",
    ),
}


def main():
    for fp, (apex_marker, impex_marker) in TARGETS.items():
        with open(fp, encoding="utf-8") as f:
            content = f.read()

        content, ok1 = remove_balanced_div(content, apex_marker)
        content, ok2 = remove_balanced_div(content, impex_marker)
        content = content.replace(
            "D2G FOODSTUFF TRADING L.L.C", "OM EXPORTER INTERNATIONAL"
        )

        with open(fp, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"{fp}: removed apex={ok1} removed as-impex={ok2}")


if __name__ == "__main__":
    main()
