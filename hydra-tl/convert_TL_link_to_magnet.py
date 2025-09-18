import json
import requests
import os
import subprocess
import tempfile

# CONFIG
INPUT_FILE = "torrents.json"
OUTPUT_FILE = "usable_json_with_magnets_and_passkey.json"
COOKIE_STRING = "PHPSESSID=YOURPHPSESSID; tluid=YOURtluid; tlpass=YOURtlpass"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)",
    "Cookie": COOKIE_STRING,
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "X-Requested-With": "XMLHttpRequest",
    "Referer": "https://www.torrentleech.org/torrents/browse/index/categories/17"
}
TORRENT2MAGNET = "../torrent2magnet/torrent2magnet.py"

with open(INPUT_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

downloads = data["downloads"]

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.write(f'{{"name": "{data["name"]}", "downloads": [\n')
    first = True

    for idx, entry in enumerate(downloads, 1):
        print(f"Torrent processing {idx}/{len(downloads)} : {entry['title']}")
        torrent_url = entry["uris"][0] if entry["uris"] else None
        new_entry = entry.copy()

        if torrent_url:
            try:
                # Temporarily download the .torrent file
                r = requests.get(torrent_url, headers=HEADERS, timeout=30)
                r.raise_for_status()
                with tempfile.NamedTemporaryFile(delete=False, suffix=".torrent") as tf:
                    tf.write(r.content)
                    temp_torrent_path = tf.name

                # Convert to magnet
                result = subprocess.run(
                    ["python", TORRENT2MAGNET, temp_torrent_path],
                    capture_output=True, text=True
                )

                if result.returncode == 0:
                    magnet_link = result.stdout.strip()
                    new_entry["uris"] = [magnet_link]
                else:
                    print(f"Error torrent2magnet: {result.stderr}")

                os.remove(temp_torrent_path)

            except Exception as e:
                print(f"Error with {entry['title']}: {e}")

        if not first:
            f.write(",\n")
        f.write(json.dumps(new_entry, ensure_ascii=False, indent=2))
        f.flush()
        first = False

    f.write("\n]}")
print(f"Conversion of torrent links to magnet links completed successfully and saved in {OUTPUT_FILE}")
