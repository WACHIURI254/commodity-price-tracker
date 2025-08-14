# scraper.py
import json
import os
from datetime import datetime
from playwright.sync_api import sync_playwright

# ----------------------
# Configuration
# ----------------------
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

STORES = [
    {"name": "Naivas", "url": "https://naivas.online/"},
    {"name": "Quickmart", "url": "https://www.quickmart.co.ke/"},
    {"name": "Carrefour", "url": "https://www.carrefour.ke/mafken/en/"},
    {"name": "Jumia", "url": "https://www.jumia.co.ke/"},
    {"name": "Greenspoon", "url": "https://greenspoon.co.ke/"}
]

OUTPUT_FILE = "prices.json"

# ----------------------
# Helper Functions
# ----------------------
def load_historical_prices():
    if os.path.exists(OUTPUT_FILE):
        with open(OUTPUT_FILE, "r") as f:
            return json.load(f)
    return []

def save_prices(prices):
    with open(OUTPUT_FILE, "w") as f:
        json.dump(prices, f, indent=2)

def scrape_store(store_name, store_url):
    # Placeholder for real scraping logic
    # Replace with Playwright scraping per store
    from random import randint
    scraped_prices = []
    for c in COMMODITIES:
        scraped_prices.append({
            "timestamp": datetime.now().isoformat(),
            "store": store_name,
            "commodity_name": c["name"],
            "unit": c["unit"],
            "price": randint(50, 5000)  # simulate a price
        })
    return scraped_prices

# ----------------------
# Main Scraper
# ----------------------
def main():
    historical_prices = load_historical_prices()
    all_prices_today = []

    with sync_playwright() as p:
        for store in STORES:
            store_prices = scrape_store(store['name'], store['url'])
            all_prices_today.extend(store_prices)

    # Append new prices to historical data
    historical_prices.extend(all_prices_today)

    # Save updated historical data
    save_prices(historical_prices)
    print(f"Scraped and saved {len(all_prices_today)} prices.")

if __name__ == "__main__":
    main()
