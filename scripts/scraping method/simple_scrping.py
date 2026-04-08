# strategy_1_basic.py
import requests
from bs4 import BeautifulSoup
import csv

def scrape_static_page(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        results = []
        
         
         # 1. Get the main parent by ID (Your reliable landmark)
        main_box = soup.find(id="POI_LIST_BOX")

        if main_box:
            # 2. Find all items (the div > a > div structure)
            # This reaches the individual cards
            items = main_box.select('div > a > div')

            for item in items:

                title_el = None
                rate_el = None
                desc_el = None
                            # 3. Choose the specific side (the "Right" cell)
                # Using [class*="..."] to ignore the random hash at the end
                right_cell = item.select_one('div[class*="OnlinePoiCell_right"]')
                        
                if right_cell:

                    # Entering another div to reach elements as you described
                    content_wrapper = right_cell.select_one('div')
                    
                    if content_wrapper:
                        # Title: Entering div > div > h2
                        title_el = content_wrapper.select_one('div > div > h2')
                        # Rate: Entering div > div > div > span
                        rate_el = content_wrapper.select_one('div > div > div > span[class*="XReviewScoreV2_score_text_Weak"]')                 
                        # Description: Entering div > span with specific class
                        desc_el = content_wrapper.select_one('div > span[class*="Comment_commentText"]')

                
                results.append({
                            "name": title_el.get_text(strip=True) if title_el else "N/A",
                            "rating": rate_el.get_text() if rate_el else "N/A",
                            "description": desc_el.get_text(strip=True) if desc_el else "N/A"
                        })
            
        return results
    except requests.RequestException as e:
        print(f"Error: {e}")
        return []




def save_to_csv( data ,filename):
    if not data :
        return 
    keys  = data[0].keys()
    with  open(filename , 'w' , encoding='utf-8' ) as f:
        writer = csv.DictWriter(f , fieldnames=keys)
        writer.writeheader()
        writer.writerows(data)   

# Example usage
if __name__ == "__main__":
    # Using a safe example site
    result = scrape_static_page('https://www.trip.com/travel-guide/attraction/algiers-20448/tourist-attractions/?locale=en-XX&curr=USD')
    save_to_csv(result , 'test5.csv')
