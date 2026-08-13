import os
import re

BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "mirror"))

GREEN = "#1B5E3F"    # Deep Forest Green -- logo/headers/primary buttons
NAVY = "#1A2332"     # Charcoal Navy -- wordmark/headings/dark text/nav
GOLD = "#D4A24E"     # Warm Amber/Gold -- CTA highlights, icons, hovers, badges
OFFWHITE = "#F7F4EE" # Warm Off-White -- page backgrounds
SAGE = "#DDE5DD"     # Light Sage Grey -- dividers, light borders/backgrounds
SLATE = "#5C6672"    # Slate Grey -- secondary/body text

# old hex -> new hex. Keys matched case-insensitively, longest-safe since all are 6 hex digits.
COLOR_MAP = {
    # primary green (buttons, borders, brand)
    "306A38": GREEN,
    "8CB46C": GREEN,
    # charcoal navy (headings, dark text, nav)
    "223645": NAVY,
    "030303": NAVY,
    "333333": NAVY,
    "383838": NAVY,
    "111111": NAVY,
    "1A1A1A": NAVY,
    "222222": NAVY,
    "31245B": NAVY,
    "273171": NAVY,
    # gold (accents, hovers, badges, kicker text)
    "086ABD": GOLD,
    "EB5A3E": GOLD,
    "E12454": GOLD,
    "FF7236": GOLD,
    "61CE70": GOLD,
    "6EC1E4": GREEN,
    # slate grey (secondary/body text)
    "647589": SLATE,
    "656565": SLATE,
    "767676": SLATE,
    "7A7A7A": SLATE,
    "A6A6A6": SLATE,
    "B7B7B7": SLATE,
    "414141": SLATE,
    "555555": SLATE,
    "54595F": SLATE,
    "0051A5": SLATE,
    # light sage grey (dividers, light borders/backgrounds)
    "D8E5EC": SAGE,
    "DDDDDD": SAGE,
    "E6E6E6": SAGE,
    "EBEBEB": SAGE,
    # warm off-white (page/section backgrounds)
    "F8F8F8": OFFWHITE,
    "F4F4F4": OFFWHITE,
    "F5F5F5": OFFWHITE,
    "FBFBFB": OFFWHITE,
    "F1F1F1": OFFWHITE,
    "F4FAFA": OFFWHITE,
}

PATTERN = re.compile("#(" + "|".join(COLOR_MAP.keys()) + ")", re.IGNORECASE)


def repl(m):
    return COLOR_MAP[m.group(1).upper()]


def main():
    changed = 0
    total = 0
    targets = []
    for root, _dirs, files in os.walk(BASE):
        for name in files:
            if name.endswith((".html", ".css")):
                targets.append(os.path.join(root, name))

    for fp in targets:
        total += 1
        with open(fp, encoding="utf-8", errors="ignore") as f:
            content = f.read()
        new_content, n = PATTERN.subn(repl, content)
        if n:
            with open(fp, "w", encoding="utf-8") as f:
                f.write(new_content)
            changed += 1

    print(f"Scanned {total} html/css files, modified {changed}.")


if __name__ == "__main__":
    main()
