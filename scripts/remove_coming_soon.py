import os
import re

BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "mirror"))

# Matches the exact block inserted by add_coming_soon.py: the overlay div
# through the trailing </style> tag, right after <body ...>.
PATTERN = re.compile(
    r'<div id="d2g-coming-soon-overlay".*?</style>\n?',
    re.DOTALL,
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
            new_content, n = PATTERN.subn("", content)
            if n:
                with open(fp, "w", encoding="utf-8") as f:
                    f.write(new_content)
                changed += 1
    print(f"Scanned {total} html files, removed overlay from {changed}.")


if __name__ == "__main__":
    main()
