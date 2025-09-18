import json
from datetime import datetime

# CONFIG
INPUT_FILE = "json_to_normalize.json"
OUTPUT_FILE = "json_normalized.json"

def human_readable_size(size_bytes: int) -> str:
    """Converts a size in bytes to a readable format (KB, MB, GB, TB)"""
    if size_bytes == 0:
        return "0 B"
    units = ["B", "KB", "MB", "GB", "TB"]
    i = 0
    size = float(size_bytes)
    while size >= 1024 and i < len(units) - 1:
        size /= 1024
        i += 1
    return f"{size:.2f} {units[i]}".replace(".00", "")

def transform_game(item: dict) -> dict:
    dt = datetime.strptime(item["date"], "%Y-%m-%d %H:%M")
    iso_date = dt.strftime("%Y-%m-%dT%H:%M:%S.000Z")
    return {
        "title": item["filename"],
        "uris": [item["link"]],
        "uploadDate": iso_date,
        "fileSize": human_readable_size(item["size"])
    }

if __name__ == "__main__":
    with open(INPUT_FILE, "r", encoding="utf-8") as f_in, \
         open(OUTPUT_FILE, "w", encoding="utf-8") as f_out:

        raw_data = json.load(f_in)

        f_out.write('{\n  "name": "kevinj93 Complete Collection (Scene + GOG)",\n  "downloads": [\n')

        for idx, item in enumerate(raw_data, start=1):
            game = transform_game(item)
            json.dump(game, f_out, ensure_ascii=False)

            if idx != len(raw_data):
                f_out.write(",\n")
            else:
                f_out.write("\n")

        f_out.write("  ]\n}")
    print("Finish!")
