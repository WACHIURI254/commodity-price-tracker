from playwright.sync_api import sync_playwright
from playwright_stealth import stealth_sync
import json
from datetime import datetime

def scrape_jumia():
    search_terms = ["maize flour", "sugar", "rice"]
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

        for term in search_terms:
            print(f"🔍 Scraping: {term}")
            url = f"https://www.jumia.co.ke/catalog/?q={term.replace(' ', '+')}"
            page.goto(url, wait_until="domcontentloaded")
            page.wait_for_selector(".prd")

            for product in page.query_selector_all(".prd"):
                name = product.query_selector(".name")
                price = product.query_selector(".prc")

                if name and price:
                    all_products.append({
                        "store": "Jumia",
                        "search_term": term,
                        "item": name.inner_text().strip(),
                        "price": price.inner_text().strip(),
                        "scraped_at": datetime.utcnow().isoformat()
                    })

        browser.close()

    # Save to prices.json
    with open("prices.json", "w", encoding="utf-8") as f:
        json.dump(all_products, f, ensure_ascii=False, indent=2)

    print(f"✅ Scraped {len(all_products)} items from Jumia.")

if __name__ == "__main__":
    scrape_jumia()
