# scraper.py
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import json
import time

def scrape_jumia():
    items = []
    url = "https://www.jumia.co.ke/mlp-groceries/?page=1"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        page.goto(url, timeout=60000)
        time.sleep(3)  # Wait for products to load fully

        html = page.content()
        soup = BeautifulSoup(html, "html.parser")

        products = soup.select("article.prd")  # Jumia's product container

        for product in products:
            name_tag = product.select_one("h3.name")
            price_tag = product.select_one("div.prc")

            if name_tag and price_tag:
                name = name_tag.get_text(strip=True)
                price = price_tag.get_text(strip=True)
                items.append({
                    "store": "Jumia",
                    "item": name,
                    "price": price
                })

        browser.close()

    return items

if __name__ == "__main__":
    data = scrape_jumia()

    with open("prices.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print("Scraped data saved to prices.json")
