import requests
import json

# For have "" and beginning and end, and ',' at end use mytexttools
# https://mytexttools.com/insert-prefix-suffix-into-line.html
# write in prefix: "
# write in suffix: ",
# click on insert and just delete the last ','
urls = [
"https://1fichier.com/dir/link1",
"https://1fichier.com/dir/link2",
]

OUTPUT_FILE = "json_to_normalize.json"

all_files = []

for url in urls:
    json_url = f"{url}?json=1|2"
    
    try:
        response = requests.get(json_url)
        response.raise_for_status()
        
        data = response.json()
        
        if isinstance(data, list):
            all_files.extend(data)
        
    except requests.exceptions.RequestException as e:
        print(f"Error retrieving {json_url}: {e}")

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(all_files, f, ensure_ascii=False, indent=4)

print(f"JSON create and save in: {OUTPUT_FILE}")
