import json

# CONFIG
INPUT = "torrents_magnets_without_trackers.json"
OUTPUT = "usable_json_with_magnets_and_trackers.json"
PASSKEY = "7ca1ff0e24354286cd445b255980dc45"

TRACKERS = [
    f"https://tracker.torrentleech.org/a/{PASSKEY}/announce",
    f"https://tracker.tleechreload.org/a/{PASSKEY}/announce"
]

with open(INPUT, "r", encoding="utf-8") as f:
    data = json.load(f)

def add_trackers(uri):
    for tracker in TRACKERS:
        uri += f"&tr={tracker}"
    return uri

for download in data.get("downloads", []):
    download["uris"] = [add_trackers(uri) for uri in download.get("uris", [])]

with open(OUTPUT, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print(f"The magnets have been updated with the trackers and saved in {OUTPUT}.")