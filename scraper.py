from playwright.sync_api import sync_playwright
from playwright_stealth import stealth_sync
import json
from datetime import datetime

def scrape_jumia():
    with sync_playwright() as p:
        # Launch Chromium in headless mode
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                       "(KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
            viewport={"width": 1366, "height": 768},
            locale="en-US",
            timezone_id="Africa/Nairobi"
        )

        page = context.new_page()

        # Apply stealth mode to avoid detection
        stealth_sync(page)

        # Go to Jumia search results for Maize Flour
        page.goto("https://www.jumia.co.ke/catalog/?q=maize+flour", wait_until="domcontentloaded")

        # Wait for products to load
        page.wait_for_selector(".prd")

        products = []
        for product in page.query_selector_all(".prd"):
            name = product.query_selector(".name")
            price = product.query_selector(".prc")

            if name and price:
                products.append({
                    "store": "Jumia",
                    "item": name.inner_text().strip(),
                    "price": price.inner_text().strip(),
                    "scraped_at": datetime.utcnow().isoformat()
                })

        browser.close()

        # Save to prices.json
        with open("prices.json", "w", encoding="utf-8") as f:
            json.dump(products, f, ensure_ascii=False, indent=2)

        print(f"Scraped {len(products)} items from Jumia.")

if __name__ == "__main__":
    scrape_jumia()
