import os

BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "mirror"))

FILES = [
    os.path.join(BASE, "feed", "index.html"),
    os.path.join(BASE, "author", "admin", "feed", "index.html"),
    os.path.join(BASE, "category", "bombay-foodstuff-trading", "feed", "index.html"),
]

REPLACEMENTS = [
    (
        "Role of D2G Foodstuff trading L.L.C With over 25 years of experience, [&#8230;]",
        "Role of D2G Foodstuff trading L.L.C Licensed by the Dubai Department of Economy &amp; Tourism, [&#8230;]",
    ),
    (
        '<p class="wp-block-paragraph">With over 25 years of experience, we specialize in <strong>spices, dry fruits, pulses, grains, oil seeds, and herbs</strong>, supplying to hotels, hypermarkets, and global importers with quality and efficiency.<strong>Conclusion</strong><strong><br></strong> The UAE is not just a trading hub but a <strong>gateway to global food markets</strong>, and companies like D2G Foodstuff trading L.L.C continue to drive this success.</p>',
        '<p class="wp-block-paragraph">Licensed by the Dubai Department of Economy &amp; Tourism, we specialize in <strong>spices, grains, pulses, dairy, meat, eggs, flour, ghee &amp; vegetable oils, and fresh &amp; dried fruits and vegetables</strong>, supplying to hotels, hypermarkets, and global importers with quality and efficiency.<strong>Conclusion</strong><strong><br></strong> The UAE is not just a trading hub but a <strong>gateway to global food markets</strong>, and companies like D2G Foodstuff trading L.L.C continue to drive this success.</p>',
    ),
]


def main():
    for fp in FILES:
        if not os.path.isfile(fp):
            print(f"missing: {fp}")
            continue
        with open(fp, encoding="utf-8") as f:
            content = f.read()
        original = content
        for old, new in REPLACEMENTS:
            content = content.replace(old, new)
        if content != original:
            with open(fp, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"updated: {fp}")
        else:
            print(f"no match: {fp}")


if __name__ == "__main__":
    main()
