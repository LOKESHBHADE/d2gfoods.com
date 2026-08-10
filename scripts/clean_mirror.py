import os
import re

BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "mirror"))

BINARY_EXT = {
    ".png", ".jpg", ".jpeg", ".gif", ".webp", ".ico", ".svg",
    ".woff", ".woff2", ".ttf", ".eot", ".otf", ".mp4", ".pdf", ".zip",
}

DUMMY_PHONE_DISPLAY = "+971-4-000-0000"
DUMMY_PHONE_TEL = "+971-4-000-0000"
DUMMY_EMAIL = "info@example.com"
DUMMY_ADDRESS_1 = "Bombay Foodstuff Trading Co. LLC 123 Business Street, Dubai - United Arab Emirates, 00000"
DUMMY_ADDRESS_2 = "Bombay Foodstuff Trading Co. LLC, 123 Business Street, Dubai - Dubai - United Arab Emirates"
DUMMY_MAP_QUERY = (
    "Bombay%20Foodstuff%20Trading%20Co.%20LLC%2C%20123%20Business%20"
    "Street%2C%20Dubai%20-%20Dubai%20-%20United%20Arab%20Emirates"
)

# (pattern, replacement, flags)
BLOCK_REMOVALS = [
    # header logo widget -> up to next sibling (nav menu container)
    (r'<div class="elementor-element elementor-element-202a4f6.*?(?=<div class="elementor-element elementor-element-c613251)', "", re.DOTALL),
    # desktop footer logo widget -> up to next sibling (text-editor description)
    (r'<div class="elementor-element elementor-element-6049b31.*?(?=<div class="elementor-element elementor-element-5205ff0)', "", re.DOTALL),
    # mobile footer logo widget -> up to next sibling (text-editor description)
    (r'<div class="elementor-element elementor-element-f9793b1.*?(?=<div class="elementor-element elementor-element-24981f7)', "", re.DOTALL),
    # favicon / apple-touch-icon / msapplication tags referencing the logo
    (r'<(?:link|meta)[^>]*cropped-hd-logo-square[^>]*/?>\s*', "", re.IGNORECASE),
    # any remaining stray logo <img> tags
    (r'<img[^>]*(?:hd-logo-square|cropped-hd-logo|logo-2\.png)[^>]*/?>', "", re.IGNORECASE),
]

# applied after TEXT_REPLACEMENTS, once hrefs pointing at the old domain have been emptied
CLEANUP_REMOVALS = [
    (r'<a[^>]*href=""[^>]*>\s*</a>', "", 0),
]

TEXT_REPLACEMENTS = [
    ("https://bombayfoodstuff.com", ""),
    ("http://bombayfoodstuff.com", ""),
    ("tel:+971-4-225-1330", f"tel:{DUMMY_PHONE_TEL}"),
    ("+971-4-225-1330", DUMMY_PHONE_DISPLAY),
    ("tel:+971-4-225-1340", f"tel:{DUMMY_PHONE_TEL}"),
    ("+971-4-225-1340", DUMMY_PHONE_DISPLAY),
    ("mailto:admin@bombayfood.ae", f"mailto:{DUMMY_EMAIL}"),
    ("admin@bombayfood.ae", DUMMY_EMAIL),
    ("mailto:bombay@eim.ae", f"mailto:{DUMMY_EMAIL}"),
    ("bombay@eim.ae", DUMMY_EMAIL),
    (
        "Bombay Foodstuff Trading Co. LLC Shop No. 17, Hawai Building, Al Ras Deira - Dubai - United Arab Emirates, 29603",
        DUMMY_ADDRESS_1,
    ),
    (
        "Bombay Foodstuff Trading Co. LLC, Shop No. 17, Hawai Building, Al Street, Al Ras Deira، dubai - Dubai - United Arab Emirates",
        DUMMY_ADDRESS_2,
    ),
    (
        "Bombay%20Foodstuff%20Trading%20Co.%20LLC%2C%20Shop%20No.%2017%2C%20Hawai%20Building%2C%20Al%20Street%2C%20Al%20Ras%20Deira%D8%8C%20dubai%20-%20Dubai%20-%20United%20Arab%20Emirates",
        DUMMY_MAP_QUERY,
    ),
]


def process(path):
    ext = os.path.splitext(path)[1].lower()
    if ext in BINARY_EXT:
        return False
    try:
        with open(path, encoding="utf-8") as f:
            content = f.read()
    except (UnicodeDecodeError, IsADirectoryError):
        return False

    original = content

    for pattern, repl, flags in BLOCK_REMOVALS:
        content = re.sub(pattern, repl, content, flags=flags)

    for old, new in TEXT_REPLACEMENTS:
        content = content.replace(old, new)

    for pattern, repl, flags in CLEANUP_REMOVALS:
        content = re.sub(pattern, repl, content, flags=flags)

    if content != original:
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return True
    return False


def main():
    changed = 0
    total = 0
    for root, _dirs, files in os.walk(BASE):
        for name in files:
            fp = os.path.join(root, name)
            total += 1
            if process(fp):
                changed += 1
    print(f"Scanned {total} files, modified {changed}.")


if __name__ == "__main__":
    main()
