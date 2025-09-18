import json
import re

# CONFIG
INPUT_FILE = "usable_json_with_magnets_and_passkey.json"
OUTPUT_FILE = "torrents_magnets_without_trackers.json"

with open(INPUT_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

def clean_uri(uri):
    return re.sub(r'&tr=[^&]*', '', uri)

for download in data.get("downloads", []):
    download["uris"] = [clean_uri(uri) for uri in download.get("uris", [])]

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print(f"The URIs have been cleaned up and saved in {INPUT_FILE}.")
