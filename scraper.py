from playwright.sync_api import sync_playwright
from playwright_stealth import stealth_sync
import json
from datetime import datetime

SEARCH_TERMS = [
    ("sugar", "sugar"),
    ("maize flour", "maize+flour"),
    ("rice", "rice")
]

def scrape_jumia():
    all_products = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                       "(KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
            viewport={"width": 1366, "height": 768},
            locale="en-US",
            timezone_id="Africa/Nairobi"
        )

        page = context.new_page()
        stealth_sync(page)

        for label, query in SEARCH_TERMS:
            print(f"🔍 Scraping prices for {label}...")

            page.goto(f"https://www.jumia.co.ke/catalog/?q={query}", wait_until="domcontentloaded")
            page.wait_for_selector(".prd", timeout=10000)

            for product in page.query_selector_all(".prd"):
                name = product.query_selector(".name")
                price = product.query_selector(".prc")

                if name and price:
                    all_products.append({
                        "store": "Jumia",
                        "category": label,
                        "item": name.inner_text().strip(),
                        "price": price.inner_text().strip(),
                        "scraped_at": datetime.utcnow().isoformat()
                    })

        browser.close()

    # Save fresh data, replacing old file
    with open("prices.json", "w", encoding="utf-8") as f:
        json.dump(all_products, f, ensure_ascii=False, indent=2)

    print(f"\n✅ Scraped {len(all_products)} total products from Jumia.")

if __name__ == "__main__":
    scrape_jumia()
