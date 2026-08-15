import os

BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "mirror"))

OLD = (
    'alt="D2G Foodstuff logo"/></a></div></div></div>'
    '<div class="elementor-element elementor-element-c613251'
)
NEW = (
    'alt="D2G Foodstuff logo"/></a></div></div></div></div>'
    '<div class="elementor-element elementor-element-c613251'
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
            new_content, n = content.replace(OLD, NEW), content.count(OLD)
            if n:
                with open(fp, "w", encoding="utf-8") as f:
                    f.write(new_content)
                changed += 1
    print(f"Scanned {total} html files, fixed {changed}.")


if __name__ == "__main__":
    main()
