import os

BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "mirror"))
LOGO_SRC = "/wp-content/uploads/2025/08/d2g-logo-placeholder.svg"

HEADER_SNIPPET = (
    '<div class="elementor-element elementor-widget elementor-widget-bew-elements-site-logo" '
    'data-widget_type="bew-elements-site-logo.default">'
    '<div class="elementor-widget-container">'
    '<div class="bew-site-logo">'
    f'<a href="/"><img class="bew-site-logo-img" src="{LOGO_SRC}" alt="D2G Foodstuff logo"/></a>'
    "</div></div></div>"
)

FOOTER_DESKTOP_SNIPPET = (
    '<div class="elementor-element elementor-widget elementor-widget-image" data-widget_type="image.default">'
    f'<a href="/"><img width="300" height="289" src="{LOGO_SRC}" alt="D2G Foodstuff logo"/></a>'
    "</div>"
)

FOOTER_MOBILE_SNIPPET = (
    '<div class="elementor-element elementor-widget elementor-widget-image" data-widget_type="image.default">'
    f'<img width="300" height="289" src="{LOGO_SRC}" alt="D2G Foodstuff logo"/>'
    "</div>"
)

INSERTIONS = [
    ('<div class="elementor-element elementor-element-c613251', HEADER_SNIPPET),
    ('<div class="elementor-element elementor-element-5205ff0', FOOTER_DESKTOP_SNIPPET),
    ('<div class="elementor-element elementor-element-24981f7', FOOTER_MOBILE_SNIPPET),
]


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
            if LOGO_SRC in content:
                continue
            original = content
            for marker, snippet in INSERTIONS:
                idx = content.find(marker)
                if idx != -1:
                    content = content[:idx] + snippet + content[idx:]
            if content != original:
                with open(fp, "w", encoding="utf-8") as f:
                    f.write(content)
                changed += 1
    print(f"Scanned {total} html files, inserted logo into {changed}.")


if __name__ == "__main__":
    main()
