from playwright.sync_api import sync_playwright, TimeoutError
from playwright_stealth import stealth_sync
import json
from datetime import datetime
import time
import random

# Configuration
SEARCH_TERMS = ["maize flour", "sugar", "rice"]
BASE_URL = "https://www.jumia.co.ke"
OUTPUT_FILE = "prices.json"
MAX_RETRIES = 3
RETRY_DELAY = 2  # seconds
SCROLL_PAUSE_TIME = 1  # seconds

# Commodity mapping
COMMODITY_MAPPING = {
    "maize flour": {
        "commodity_id": "maize_flour",
        "name": "Maize Flour",
        "category": "Staples",
        "canonical_unit": "2kg"
    },
    "sugar": {
        "commodity_id": "sugar",
        "name": "Sugar",
        "category": "Staples",
        "canonical_unit": "2kg"
    },
    "rice": {
        "commodity_id": "rice",
        "name": "Rice",
        "category": "Staples",
        "canonical_unit": "2kg"
    }
}

def scrape_jumia():
    all_products = []
    
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=["--disable-blink-features=AutomationControlled"]
        )
        
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
            viewport={"width": 1366, "height": 768},
            locale="en-US",
            timezone_id="Africa/Nairobi",
            extra_http_headers={
                "Accept-Language": "en-US,en;q=0.9",
                "Accept-Encoding": "gzip, deflate, br",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            }
        )
        
        page = context.new_page()
        stealth_sync(page)
        
        for term in SEARCH_TERMS:
            print(f"🔍 Scraping: {term}")
            url = f"{BASE_URL}/catalog/?q={term.replace(' ', '+')}"
            
            for attempt in range(MAX_RETRIES):
                try:
                    page.goto(url, wait_until="domcontentloaded", timeout=30000)
                    
                    # Random scroll to simulate human behavior
                    for _ in range(random.randint(1, 3)):
                        page.mouse.wheel(0, random.randint(300, 600))
                        time.sleep(SCROLL_PAUSE_TIME)
                    
                    # Wait for products to load
                    page.wait_for_selector(".prd", timeout=15000)
                    
                    # Get all products
                    products = page.query_selector_all(".prd")
                    print(f"Found {len(products)} products for {term}")
                    
                    if not products:
                        print(f"No products found for {term}, skipping...")
                        continue
                    
                    commodity_info = COMMODITY_MAPPING.get(term.lower(), {})
                    
                    for product in products:
                        try:
                            name_elem = product.query_selector(".name")
                            price_elem = product.query_selector(".prc")
                            link_elem = product.query_selector("a.core")
                            
                            if name_elem and price_elem:
                                name = name_elem.inner_text().strip()
                                price_text = price_elem.inner_text().strip()
                                
                                # Clean price text
                                price = price_text.replace("KSh", "").replace(",", "").strip()
                                
                                # Get product URL
                                product_url = ""
                                if link_elem:
                                    product_url = BASE_URL + link_elem.get_attribute("href")
                                
                                all_products.append({
                                    "commodity_id": commodity_info.get("commodity_id", term.replace(" ", "_")),
                                    "commodity_name": commodity_info.get("name", name),
                                    "category": commodity_info.get("category", "Other"),
                                    "canonical_unit": commodity_info.get("canonical_unit", "1kg"),
                                    "store": "Jumia",
                                    "item": name,
                                    "price": float(price) if price.replace('.', '', 1).isdigit() else 0,
                                    "unit_price": float(price) if price.replace('.', '', 1).isdigit() else 0,
                                    "product_url": product_url,
                                    "in_stock": True,  # Assuming all found products are in stock
                                    "scraped_at": datetime.utcnow().isoformat()
                                })
                        except Exception as e:
                            print(f"Error processing product: {e}")
                            continue
                    
                    # Success - break out of retry loop
                    break
                    
                except TimeoutError:
                    print(f"Timeout on attempt {attempt + 1} for {term}")
                    if attempt < MAX_RETRIES - 1:
                        time.sleep(RETRY_DELAY * (attempt + 1))
                    else:
                        print(f"Max retries reached for {term}, skipping...")
                except Exception as e:
                    print(f"Error scraping {term}: {e}")
                    if attempt < MAX_RETRIES - 1:
                        time.sleep(RETRY_DELAY * (attempt + 1))
                    else:
                        print(f"Max retries reached for {term}, skipping...")
        
        browser.close()
    
    # Save to JSON file
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(all_products, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Scraped {len(all_products)} items from Jumia.")
    return all_products

if __name__ == "__main__":
    scrape_jumia()
