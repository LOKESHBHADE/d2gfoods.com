import os
import re

BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "mirror"))
TARGET = os.path.join(BASE, "product-range", "index.html")

# title -> image filename
IMAGES = {
    "Dairy Products": "dairy-products.jpg",
    "Fresh, Chilled &amp; Frozen Meat": "fresh-chilled-frozen-meat.jpg",
    "Eggs": "eggs.jpg",
    "Flour": "flour.jpg",
    "Ghee &amp; Vegetable Oil": "ghee-vegetable-oil.jpg",
    "Fresh Vegetables &amp; Fruits": "fresh-vegetables-fruits.jpg",
    "Potatoes": "potatoes.jpg",
}

PLACEHOLDER_RE = re.compile(
    r'<div style="height:160px;background:#DDE5DD;border-bottom:2px dashed #5C6672;'
    r'display:flex;align-items:center;justify-content:center;color:#5C6672;font-size:14px;'
    r'font-family:Arial,Helvetica,sans-serif;text-align:center;padding:0 16px;">'
    r"Product photo coming soon</div>\s*"
    r'<div style="padding:20px;">\s*'
    r'<h3 style="color:#1A2332;font-size:18px;margin:0 0 8px;font-family:Arial,Helvetica,sans-serif;">'
    r"([^<]+)</h3>",
    re.DOTALL,
)


def replacement(m):
    title = m.group(1)
    img = IMAGES.get(title)
    if not img:
        return m.group(0)
    img_tag = (
        f'<div style="height:160px;overflow:hidden;">'
        f'<img src="/wp-content/uploads/2025/10/{img}" alt="{title}" '
        f'style="width:100%;height:100%;object-fit:cover;display:block;"/></div>'
        f'<div style="padding:20px;">'
        f'<h3 style="color:#1A2332;font-size:18px;margin:0 0 8px;font-family:Arial,Helvetica,sans-serif;">{title}</h3>'
    )
    return img_tag


def main():
    with open(TARGET, encoding="utf-8") as f:
        content = f.read()
    new_content, n = PLACEHOLDER_RE.subn(replacement, content)
    with open(TARGET, "w", encoding="utf-8") as f:
        f.write(new_content)
    print(f"Replaced {n} placeholder cards with real images.")


if __name__ == "__main__":
    main()
