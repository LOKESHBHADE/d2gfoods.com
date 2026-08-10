import os
import re

BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "mirror"))

DIV_TAG_RE = re.compile(r"<div\b|</div>")


def remove_balanced_div(content, marker):
    """Remove the full <div ...>...</div> that contains `marker`, matching balanced div depth."""
    idx = content.find(marker)
    if idx == -1:
        return content, False
    start = content.rfind("<div", 0, idx)
    if start == -1:
        return content, False
    depth = 0
    pos = start
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


TARGETS = {
    "index.html": ["elementor-element-272fb845", "elementor-element-2426b62"],
    os.path.join("about-us", "index.html"): ["elementor-element-6c1b059", "elementor-element-f82cd6a"],
}


def main():
    for rel_path, markers in TARGETS.items():
        fp = os.path.join(BASE, rel_path)
        with open(fp, encoding="utf-8") as f:
            content = f.read()
        for marker in markers:
            content, ok = remove_balanced_div(content, marker)
            print(f"{rel_path}: removed block for {marker}: {ok}")
        with open(fp, "w", encoding="utf-8") as f:
            f.write(content)


if __name__ == "__main__":
    main()
