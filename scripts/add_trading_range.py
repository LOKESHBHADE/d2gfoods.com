# -*- coding: utf-8 -*-
import os

BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "mirror"))
TARGET = os.path.join(BASE, "product-range", "index.html")
MARKER = '<div class="ekit-template-content-markup ekit-template-content-footer'

CATEGORIES = [
    ("Dairy Products", "Fresh and long-life dairy products sourced from trusted producers, supplied to retailers, hotels, and food service businesses across the UAE."),
    ("Fresh, Chilled &amp; Frozen Meat", "Quality-assured fresh, chilled, and frozen meat handled under strict cold-chain standards for reliable delivery to butchers, restaurants, and retailers."),
    ("Eggs", "Farm-fresh eggs supplied in bulk and retail quantities, meeting food safety standards for hotels, bakeries, and supermarkets."),
    ("Flour", "A range of milling-grade flours for bakeries, restaurants, and food manufacturers, supplied consistently and in bulk."),
    ("Ghee &amp; Vegetable Oil", "Premium ghee and vegetable oils trusted for cooking and food production, supplied to households and commercial kitchens alike."),
    ("Fresh Vegetables &amp; Fruits", "Seasonal fresh vegetables and fruits sourced for quality and freshness, delivered to retailers, restaurants, and wholesalers."),
    ("Potatoes", "Bulk and retail supply of quality potatoes sourced to meet the steady demand of the UAE food trade."),
]

CARD_TEMPLATE = """<div style="background:#F7F4EE;border-radius:16px;overflow:hidden;border:1px solid #DDE5DD;">
<div style="height:160px;background:#DDE5DD;border-bottom:2px dashed #5C6672;display:flex;align-items:center;justify-content:center;color:#5C6672;font-size:14px;font-family:Arial,Helvetica,sans-serif;text-align:center;padding:0 16px;">Product photo coming soon</div>
<div style="padding:20px;">
<h3 style="color:#1A2332;font-size:18px;margin:0 0 8px;font-family:Arial,Helvetica,sans-serif;">{title}</h3>
<p style="color:#5C6672;font-size:14px;line-height:1.5;margin:0;font-family:Arial,Helvetica,sans-serif;">{desc}</p>
</div>
</div>"""

cards_html = "\n".join(CARD_TEMPLATE.format(title=t, desc=d) for t, d in CATEGORIES)

SECTION = f"""<div style="max-width:1200px;margin:0 auto;padding:60px 20px;">
<div style="text-align:center;margin-bottom:40px;">
<h2 style="color:#1A2332;font-size:32px;margin:0 0 12px;font-family:Arial,Helvetica,sans-serif;">Our Complete Trading Range</h2>
<p style="color:#5C6672;font-size:16px;max-width:680px;margin:0 auto;font-family:Arial,Helvetica,sans-serif;">Beyond spices, pulses, and dry fruits, D2G Foodstuff Trading L.L.C is licensed by the Dubai Department of Economy &amp; Tourism (License No. 1642673) to trade the following categories.</p>
</div>
<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:24px;">
{cards_html}
</div>
</div>
"""


def main():
    with open(TARGET, encoding="utf-8") as f:
        content = f.read()

    if "Our Complete Trading Range" in content:
        print("Already present, skipping.")
        return

    idx = content.find(MARKER)
    if idx == -1:
        raise SystemExit("Footer marker not found; aborting.")

    content = content[:idx] + SECTION + content[idx:]

    with open(TARGET, "w", encoding="utf-8") as f:
        f.write(content)
    print("Inserted trading range section into product-range/index.html")


if __name__ == "__main__":
    main()
