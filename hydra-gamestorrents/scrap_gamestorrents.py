import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
import time
import subprocess
import os
import re

# CONFIG
BASE_URL = "https://www.gamestorrents.app/juegos-pc/page/{}/"
DOMAIN = "https://www.gamestorrents.app"
TORRENT2MAGNET = "../torrent2magnet/torrent2magnet.py"
START_PAGE = 1
END_PAGE = 536
OUTPUT_FILE = "gamestorrents.json"
NAME_MODE = "torrent" # 'listing' or 'torrent'

def get_magnet_from_torrent(torrent_url):
    """Download torrent temporarily and convert to magnet using torrent2magnet.py"""
    local_filename = "temp.torrent"
    with requests.get(torrent_url, stream=True, headers={"User-Agent": "Mozilla/5.0"}) as r:
        if r.status_code != 200:
            print(f"Failed to download torrent: {torrent_url}")
            return None
        with open(local_filename, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)

    result = subprocess.run(
        ["python", TORRENT2MAGNET, local_filename],
        capture_output=True, text=True
    )
    magnet_link = result.stdout.strip()
    os.remove(local_filename)
    return magnet_link

def normalize_name(name: str) -> str:
    clean = name.replace("&", "and")

    # Replace spaces, various dashes, colons and other punctuation by dots
    clean = re.sub(r"[ \-\–\—\:\：\!\|\[\]\(\)\_\’\,\'\"\{\}\/\\\%\@\#\~\*\$\?]", ".", name)

    # Collapse multiple dots into one
    clean = re.sub(r"\.+", ".", clean)

    # Strip leading/trailing dots
    clean = clean.strip(".")

    return clean

def scrape_game_page(url, name_mode="torrent", base_name=None):
    """Scrape individual game page to extract magnet info"""
    r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    if r.status_code != 200:
        return None
    
    soup = BeautifulSoup(r.text, "html.parser")

    torrent_tag = soup.find("a", id="download_torrent")
    if not torrent_tag:
        print(f"No torrent found for {url}")
        return None

    torrent_href = torrent_tag.get("href", "")
    if not torrent_href:
        print(f"Empty torrent href for {url}")
        return None
    if torrent_href.startswith("/"):
        torrent_href = DOMAIN + torrent_href

    magnet_link = get_magnet_from_torrent(torrent_href)
    if not magnet_link:
        print(f"Failed to get magnet link for {torrent_href}")
        return None

    if name_mode == "listing" and base_name:
        clean_name = normalize_name(base_name)
    else:
        filename = torrent_href.split("/")[-1]
        clean_name = filename.replace(".torrent", "")
        clean_name = "-".join(clean_name.split("-")[1:])

    info_list = soup.find_all("ul", class_="listencio")
    if len(info_list) < 2:
        return None
    lis = info_list[1].find_all("li")

    file_size = None
    upload_date = None
    release_name = None
    version_name = None

    for li in lis:
        text = li.get_text(strip=True)
        if text.startswith("Tamaño:"):
            file_size = li.find("strong").get_text(strip=True)
            file_size = file_size.replace(" GBs", " GB").replace(" MBs", " MB")
        elif text.startswith("Fecha:"):
            date_str = li.find("strong").get_text(strip=True)
            upload_date = datetime.strptime(date_str, "%d-%m-%Y").strftime("%Y-%m-%dT00:00:00.000Z")
        elif text.startswith("Release:"):
            release_name = li.find("strong").get_text(strip=True)
        elif text.startswith("Version:"):
            version_name = li.find("strong").get_text(strip=True)


    if name_mode == "listing":
        if version_name:
            clean_name = f"{clean_name}.{version_name}"
        if release_name:
            clean_name = f"{clean_name}-{release_name}"

    return {
        "title": clean_name,
        "uris": [magnet_link],
        "uploadDate": upload_date,
        "fileSize": file_size
    }


def scrape_all_pages(max_pages, name_mode="torrent"):
    # Old torrent from gamestorrents, don't have proper name.
    # For them, go use name_mode "listing"
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write('{"name": "GamesTorrent", "downloads": [\n')
        first = True
        
        for page in range(START_PAGE, max_pages+1):
            print(f"Scraping page {page}/{max_pages}...")
            url = BASE_URL.format(page)
            r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
            if r.status_code != 200:
                print(f"Warning: page {page} returned status {r.status_code}")
                continue

            soup = BeautifulSoup(r.text, "html.parser")
            games = soup.find_all("div", class_="col-md-2")

            for game in games:
                link_tag = game.find("a", title=True)
                if not link_tag:
                    continue
                game_link = link_tag["href"]
                base_name = link_tag["title"]

                game_data = scrape_game_page(game_link, name_mode=name_mode, base_name=base_name)
                if game_data:
                    if not first:
                        f.write(",\n")
                    f.write(json.dumps(game_data, ensure_ascii=False))
                    f.flush()
                    first = False

        f.write("\n]}")


if __name__ == "__main__":
    scrape_all_pages(END_PAGE, name_mode=NAME_MODE)
    print(f"Scraping completed. File {OUTPUT_FILE} created with magnet links.")
