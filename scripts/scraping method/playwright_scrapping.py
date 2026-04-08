from playwright.sync_api import sync_playwright
import time
from bs4 import BeautifulSoup
import csv
import random

def scrape_with_playwright(url):
    results = []
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=1000, args=["--disable-blink-features=AutomationControlled"])
        context = browser.new_context(viewport={'width': 1280, 'height': 800})
        page = context.new_page()
        
        try:
            print(f"Opening: {url}")
            page.goto(url, wait_until="domcontentloaded", timeout=0)
            page.wait_for_selector('#POI_LIST_BOX', timeout=30000)

            for page_num in range(1, 99):
                print(f"\n--- PROCESSING PAGE {page_num} ---")
                
                # 1. Scrolled Incremental Loading
                page.evaluate("window.scrollTo(0, 0)")
                for i in range(6): 
                    page.mouse.wheel(0, 1000)
                    time.sleep(1.2)
                
                # 2. Capture state before clicking
                current_html = page.content()
                soup_before = BeautifulSoup(current_html, 'html.parser')
                # Get the name of the very first item to use as a "marker"
                first_item = soup_before.select_one('h2')
                marker_name = first_item.get_text(strip=True) if first_item else ""

                # 3. Scrape current data
                soup = BeautifulSoup(page.content(), 'html.parser')
                items = soup.select('div > a > div')
                
                new_on_page = 0
                for item in items:
                    title_el = item.select_one('h2')
                    if title_el:
                        name = title_el.get_text(strip=True)
                        if not any(d['name'] == name for d in results):
                            rate_el = item.select_one('span[class*="score_text"]')
                            desc_el = item.select_one('span[class*="Comment_commentText"]')
                            results.append({
                                "name": name,
                                "rating": rate_el.get_text(strip=True) if rate_el else "N/A",
                                "description": desc_el.get_text(strip=True) if desc_el else "N/A"
                            })
                            new_on_page += 1
                
                print(f"Page {page_num}: Captured {new_on_page} items. Total: {len(results)}")

                # 4. Pagination - The Critical Part
                next_btns = page.query_selector_all('div[class*="Pagination_aside"]')
                if next_btns and next_btns[-1].is_enabled():
                    print("Clicking 'Next'...")
                    next_btns[-1].click()
                    
                    # 5. WAIT FOR CONTENT TO BE DIFFERENT
                    # Instead of a complex function, we just loop and check the H2 every second
                    changed = False
                    for _ in range(15): # Try for 15 seconds
                        time.sleep(1)
                        new_h2 = page.query_selector('h2')
                        if new_h2 and new_h2.inner_text() != marker_name:
                            print("Success: Page content changed!")
                            changed = True
                            break
                    
                    if not changed:
                        print("Warning: Page content didn't change after click. Trying to force wait...")
                        time.sleep(5) # Final desperation wait
                else:
                    print("No more pages available.")
                    break

        except Exception as e:
            print(f"Error: {e}")
        finally:
            browser.close()
            
    return results

def save_to_csv(data, filename):
    if not data: return
    keys = data[0].keys()
    with open(filename, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(data)
    print(f"File saved: {filename}")

if __name__ == "__main__":
    url = 'https://www.trip.com/travel-guide/attraction/algiers-20448/tourist-attractions/?locale=en-XX&curr=USD'
    data = scrape_with_playwright(url)
    save_to_csv(data, 'trip_algiers_final3.csv')