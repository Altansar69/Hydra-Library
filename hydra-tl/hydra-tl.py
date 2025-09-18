import json
import requests
import os
import time
from datetime import datetime

# CONFIG
OUTPUT_FILE = "torrents.json"
TEMP_FILE = "torrents_temp.json"
BASE_URL = "https://www.torrentleech.org/torrents/browse/list/categories/17/page/{page}"
START_PAGE = 1
END_PAGE = 536
COOKIE_STRING = "PHPSESSID=YOURPHPSESSID; tluid=YOURtluid; tlpass=YOURtlpass"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)",
    "Cookie": COOKIE_STRING,
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "X-Requested-With": "XMLHttpRequest",
    "Referer": "https://www.torrentleech.org/torrents/browse/index/categories/17"
}

# Load existing data if temporary file is present
if os.path.exists(TEMP_FILE):
    with open(TEMP_FILE, "r", encoding="utf-8") as f:
        results = json.load(f)
    print(f"Successful recovery. {len(results['downloads'])} downloads already retrieved.")
else:
    results = {"name": "TorrentLeech", "downloads": []}

# Loop
for page in range(START_PAGE, END_PAGE + 1):
    print(f"Retrieving page {page}")
    url = BASE_URL.format(page=page)
    try:
        r = requests.get(url, headers=HEADERS, timeout=20)
        r.raise_for_status()
        data = r.json()

        torrent_list = data.get("torrentList", [])
        for torrent in torrent_list:
            title = torrent.get("name")
            file_size_bytes = torrent.get("size", 0)
            # Convert size
            if file_size_bytes >= 1024**3:
                file_size = f"{file_size_bytes / 1024**3:.2f} GB"
            elif file_size_bytes >= 1024**2:
                file_size = f"{file_size_bytes / 1024**2:.2f} MB"
            else:
                file_size = f"{file_size_bytes} B"

            added = torrent.get("addedTimestamp")
            try:
                dt = datetime.strptime(added, "%Y-%m-%d %H:%M:%S")
                upload_date = dt.isoformat() + "Z"
            except:
                upload_date = added

            fid = torrent.get("fid")
            download_link = f"https://www.torrentleech.org/download/{fid}/{torrent.get('filename')}" if fid else None

            results["downloads"].append({
                "title": title,
                "uris": [download_link] if download_link else [],
                "uploadDate": upload_date,
                "fileSize": file_size
            })

        with open(TEMP_FILE, "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=2)

        time.sleep(0.1)

    except Exception as e:
        print(f"Error page {page}: {e}")
        time.sleep(0.2)
        continue

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

if os.path.exists(TEMP_FILE):
    os.remove(TEMP_FILE)

print(f"Scraping complete, and saved to {OUTPUT_FILE}. {len(results['downloads'])} torrents retrieved.")
