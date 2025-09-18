import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json

# CONFIG
BASE_URL = "https://www.skidrowreloaded.com/pc/?lcp_page1={}"
START_PAGE = 1
END_PAGE = 536
OUTPUT_FILE = "skidrow.json"

def parse_game_page(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")
    
    size_tag = soup.find(string=lambda t: t.strip().startswith("Size:"))
    file_size = size_tag.strip().split("Size:")[-1].strip() if size_tag else None

    uris = []
    valid_hosts = ["1FICHIER", "MEGA", "PIXELDRAIN", "MEDIAFIRE", "GOFILE", "DATANODES", "QIWI", "MAGNET LINK"]
    
    for p in soup.find_all("p"):
        strong_tag = p.find("strong")
        if strong_tag:
            host_name = strong_tag.get_text(strip=True).upper()
            if host_name in valid_hosts:
                next_a = p.find_next("a", href=True)
                if next_a:
                    uris.append(next_a['href'])
    
    return file_size, uris

def parse_main_page(page_number):
    url = BASE_URL.format(page_number)
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")
    
    game_list = soup.select("ul.lcp_catlist li")
    if not game_list:
        return None
    
    games = []
    for li in game_list:
        a_tag = li.find("a")
        title = a_tag.get_text(strip=True)
        link = a_tag['href']
        date_text = li.get_text(strip=True).replace(title, '').strip()
        try:
            upload_date = datetime.strptime(date_text, "%B %d, %Y").isoformat() + ".000Z"
        except:
            upload_date = None
        
        file_size, uris = parse_game_page(link)
        
        game_info = {
            "title": title,
            "uris": uris,
            "uploadDate": upload_date,
            "fileSize": file_size
        }
        games.append(game_info)
    return games

def scrape_all_pages(max_pages):
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write('{"name": "SkidrowReloaded", "downloads": [\n')
        first = True
        page_number = START_PAGE
        
        while page_number <= max_pages:
            print(f"Scraping page {page_number}/{max_pages}...")
            games = parse_main_page(page_number)
            if not games:
                break
            for game in games:
                if not first:
                    f.write(",\n")
                f.write(json.dumps(game, ensure_ascii=False))
                f.flush()
                first = False
            page_number += 1
        
        f.write("\n]}")
    print("Scraping completed. File skidrow.json created.")

if __name__ == "__main__":
    scrape_all_pages(END_PAGE)
