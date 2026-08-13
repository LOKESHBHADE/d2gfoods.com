import os

BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "mirror"))

REPLACEMENTS = [
    # Remove false "25+ years / modern facilities" claim (D2G is a newly formed LLC,
    # per its Memorandum of Association dated 03/08/2026) and broaden the product
    # list to match the real trade license activities.
    (
        "D2G Foodstuff trading L.L.C delivers premium spices, pulses, grains, and dry fruits worldwide. "
        "With 25+ years of expertise, modern facilities, and a trusted supply network, we ensure quality, "
        "reliability, and customer satisfaction every time.",
        "D2G Foodstuff trading L.L.C is a Dubai-licensed trading company supplying premium spices, grains, "
        "pulses, dairy products, fresh &amp; frozen meat, eggs, flour, ghee &amp; vegetable oils, and fresh &amp; "
        "dried fruits and vegetables worldwide. Backed by a trusted supply network, we ensure quality, "
        "reliability, and customer satisfaction every time.",
    ),
    # Add a licensing trust line under the footer copyright, site-wide.
    (
        "<p>© 2025 D2G Foodstuff trading L.L.C. All Rights Reserved.</p>",
        "<p>© 2025 D2G Foodstuff trading L.L.C. All Rights Reserved.</p>"
        '<p style="font-size:12px;opacity:0.8;margin-top:4px;">Licensed by the Dubai Department of Economy '
        "&amp; Tourism &mdash; License No. 1642673</p>",
    ),
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
            original = content
            for old, new in REPLACEMENTS:
                content = content.replace(old, new)
            if content != original:
                with open(fp, "w", encoding="utf-8") as f:
                    f.write(content)
                changed += 1
    print(f"Scanned {total} html files, modified {changed}.")


if __name__ == "__main__":
    main()
