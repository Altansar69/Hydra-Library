import json

# List of JSON files to merge
json_files = [
    "scene.json",
    "old_scene.json",
    "non_standard.json",
    "gog.json",
]
OUTPUT_FILE = "combined.json"

merged_downloads = []

for file_name in json_files:
    with open(file_name, "r", encoding="utf-8") as f:
        data = json.load(f)
        merged_downloads.extend(data.get("downloads", []))


with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.write('{\n  "name": "kevinj93 Complete Collection (Combined)",\n  "downloads": [\n')
    for i, item in enumerate(merged_downloads):
        json_line = json.dumps(item, ensure_ascii=False)
        if i < len(merged_downloads) - 1:
            f.write(f"    {json_line},\n")
        else:
            f.write(f"    {json_line}\n")
    f.write("  ]\n}")

print(f"Merger completed! {len(merged_downloads)} games in {OUTPUT_FILE}")
