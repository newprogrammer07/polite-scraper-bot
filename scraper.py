import time
import json
import urllib.robotparser
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup

# ==========================================
# 1. SETUP & IDENTIFICATION
# ==========================================
USER_AGENT = "MyEducationalBot/1.0 (ashutoshnayak0077@gmail.com)"
TARGET_SITE = "http://quotes.toscrape.com" # The official scraping sandbox

session = requests.Session()
session.headers.update({'User-Agent': USER_AGENT})

# ==========================================
# 2. CHECKING PERMISSIONS (robots.txt)
# ==========================================
rp = urllib.robotparser.RobotFileParser()
robots_url = urljoin(TARGET_SITE, '/robots.txt')
rp.set_url(robots_url)

try:
    rp.read()
    print("✅ Successfully read robots.txt")
except Exception as e:
    print(f"⚠️ Warning with robots.txt: {e}. Proceeding with standard politeness.")

# ==========================================
# 3. FETCHING THE WEBPAGE
# ==========================================
def fetch_page(url):
    """Downloads the webpage, politely."""
    # If robots.txt exists but blocks us, we stop.
    if rp.entries and not rp.can_fetch(USER_AGENT, url):
        print(f"❌ BLOCKED by robots.txt: {url}")
        return None

    print(f"⏳ Waiting 2 seconds before scraping {url}...")
    time.sleep(2) 

    try:
        response = session.get(url, timeout=10)
        response.raise_for_status() 
        return response.text 
    except Exception as e:
        print(f"❌ ERROR downloading {url}: {e}")
        return None

# ==========================================
# 4. EXTRACTING & CLEANING DATA
# ==========================================
def parse_and_clean(html_content, url):
    """Finds the quotes, authors, and tags, and cleans them."""
    soup = BeautifulSoup(html_content, 'html.parser')
    extracted_records = []

    # Find all the quote blocks on the page
    quote_blocks = soup.find_all('div', class_='quote')
    
    for block in quote_blocks:
        # Extract the specific fields
        text = block.find('span', class_='text').get_text(strip=True)
        author = block.find('small', class_='author').get_text(strip=True)
        
        # Extract the tags (which are in a list)
        tags_elements = block.find_all('a', class_='tag')
        tags = [tag.get_text(strip=True) for tag in tags_elements]

        # Structure the data
        extracted_records.append({
            "url": url,
            "author": author,
            "quote": text,
            "tags": tags
        })
        
    return extracted_records

# ==========================================
# 5. MAIN EXECUTION
# ==========================================
if __name__ == "__main__":
    # We will scrape the first two pages of the sandbox site
    urls_to_scrape = [
        f"{TARGET_SITE}/page/1/",
        f"{TARGET_SITE}/page/2/"
    ]

    all_scraped_data = []

    for url in urls_to_scrape:
        html = fetch_page(url)
        
        if html:
            page_data = parse_and_clean(html, url)
            all_scraped_data.extend(page_data)
            print(f"✅ Successfully extracted {len(page_data)} quotes from {url}")

    # Save everything into a structured JSON file
    output_filename = "rag_corpus.json"
    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(all_scraped_data, f, indent=4, ensure_ascii=False)
    
    print(f"🎉 All done! {len(all_scraped_data)} total records saved to {output_filename}")