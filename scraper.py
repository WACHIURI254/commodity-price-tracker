# scraper.py
import json
import os
from datetime import datetime
from playwright.sync_api import sync_playwright

# Top 50 commodities with canonical units
COMMODITIES = [
    {"name": "Maize flour", "unit": "2 kg"},
    {"name": "Wheat flour", "unit": "2 kg"},
    {"name": "Rice (long grain)", "unit": "2 kg"},
    {"name": "Sugar", "unit": "2 kg"},
    {"name": "Cooking oil (vegetable)", "unit": "1 L"},
    {"name": "Salt", "unit": "1 kg"},
    {"name": "Bread (white/standard)", "unit": "400 g"},
    {"name": "Milk (fresh)", "unit": "500 ml"},
    {"name": "Eggs", "unit": "tray of 30"},
    {"name": "Pasta/Spaghetti", "unit": "500 g"},
    {"name": "Dry beans", "unit": "1 kg"},
    {"name": "Dry maize/unga", "unit": "2 kg"},
    {"name": "Green grams (ndengu)", "unit": "1 kg"},
    {"name": "Lentils", "unit": "1 kg"},
    {"name": "Tea leaves", "unit": "250 g"},
    {"name": "Instant coffee", "unit": "100 g"},
    {"name": "Drinking chocolate/cocoa", "unit": "500 g"},
    {"name": "Peanut butter", "unit": "400 g"},
    {"name": "Jam (assorted)", "unit": "400 g"},
    {"name": "Margarine/butter spread", "unit": "500 g"},
    {"name": "Bottled water", "unit": "1.5 L"},
    {"name": "Soda (assorted)", "unit": "2 L"},
    {"name": "Cooking gas (LPG) 6 kg refill", "unit": "6 kg"},
    {"name": "Cooking gas (LPG) 13 kg refill", "unit": "13 kg"},
    {"name": "Tomatoes", "unit": "1 kg"},
    {"name": "Onions (red)", "unit": "1 kg"},
    {"name": "Potatoes", "unit": "2 kg"},
    {"name": "Carrots", "unit": "1 kg"},
    {"name": "Cabbage", "unit": "1 head (~1.5–2 kg)"},
    {"name": "Toilet paper/tissue", "unit": "10 pack"},
    {"name": "Laundry detergent powder", "unit": "1 kg"},
    {"name": "Dishwashing liquid", "unit": "750 ml"},
    {"name": "Bar soap (multipurpose)", "unit": "800 g"},
    {"name": "Bathing soap", "unit": "100 g"},
    {"name": "Toothpaste", "unit": "100 ml"},
    {"name": "Toothbrush", "unit": "single"},
    {"name": "Sanitary pads", "unit": "regular 10–12 pack"},
    {"name": "Baby diapers", "unit": "size 3, 56–60 pack"},
    {"name": "Baby wipes", "unit": "80 sheets"},
    {"name": "Petroleum jelly", "unit": "250 ml"},
    {"name": "Bleach", "unit": "1 L"},
    {"name": "Surface cleaner", "unit": "1 L"},
    {"name": "Scouring powder", "unit": "500 g"},
    {"name": "Steel wool", "unit": "6 pack"},
    {"name": "Insecticide spray", "unit": "300 ml"},
    {"name": "Matches", "unit": "10 boxes"},
    {"name": "Candles", "unit": "6 pack"},
    {"name": "Aluminum foil", "unit": "25 m"},
    {"name": "Cling film", "unit": "30 m"},
    {"name": "Trash bags", "unit": "medium 30–40 L, 30 pack"},
]

# Stores to scrape
STORES = [
    {"name": "Naivas", "url": "https://naivas.online/"},
    {"name": "Quickmart", "url": "https://www.quickmart.co.ke/"},
    {"name": "Carrefour", "url": "https://www.carrefour.ke/mafken/en/"},
    {"name": "Jumia", "url": "https://www.jumia.co.ke/"},
    {"name": "Greenspoon", "url": "https://greenspoon.co.ke/"},
]

# Output file
OUTPUT_FILE = "prices.json"

def load_existing_prices():
    if os.path.exists(OUTPUT_FILE):
        with open(OUTPUT_FILE, "r") as f:
            try:
                return json.load(f)
            except:
                return []
    return []

def save_prices(prices):
    with open(OUTPUT_FILE, "w") as f:
        json.dump(prices, f, indent=2)

def scrape_store(page, store_name, store_url):
    print(f"Scraping {store_name}...")
    results = []
    for attempt in range(3):
        try:
            page.goto(store_url, timeout=60000, wait_until="domcontentloaded")
            break
        except Exception as e:
            print(f"Attempt {attempt+1} failed for {store_name}: {e}")
            if attempt == 2:
                print(f"Skipping {store_name} due to repeated failures.")
                return results

    # Simple placeholder scraping logic
    # TODO: Replace with real selectors per store
    for commodity in COMMODITIES:
        # Example: generate random price for demo
        import random
        price = random.randint(100, 1000)
        results.append({
            "commodity": commodity["name"],
            "unit": commodity["unit"],
            "store": store_name,
            "price": price,
            "timestamp": datetime.now().isoformat()
        })
    return results

def main():
    all_prices = load_existing_prices()
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.set_extra_http_headers({"Accept-Language": "en-US,en;q=0.9"})
        page.set_user_agent(
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36"
        )

        for store in STORES:
            store_prices = scrape_store(page, store["name"], store["url"])
            all_prices.extend(store_prices)

        browser.close()
    save_prices(all_prices)
    print(f"Saved {len(all_prices)} price records to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
