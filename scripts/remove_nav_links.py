import os
import re

BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "mirror"))

# Removes the "Team" and "Certificates" <li> entries from the "Who We Are" dropdown
# (they're nested inside the "About Us" <li>, so 2 of the 3 trailing </li> come with them).
NAV_PATTERN = re.compile(
    r'<li class="menu-item menu-item-type-post_type menu-item-object-page menu-item-1876[^"]*"[^>]*>'
    r'<a class="dropdown-item" href="[^"]*">Team</a>\s*'
    r'<li class="menu-item menu-item-type-post_type menu-item-object-page menu-item-1914[^"]*"[^>]*>'
    r'<a class="dropdown-item" href="[^"]*">Certificates</a></li></li>',
    re.IGNORECASE,
)


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
            new_content, n = NAV_PATTERN.subn("", content)
            if n:
                with open(fp, "w", encoding="utf-8") as f:
                    f.write(new_content)
                changed += 1
    print(f"Scanned {total} html files, modified {changed}.")


if __name__ == "__main__":
    main()
