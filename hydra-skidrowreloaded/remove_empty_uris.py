import json

INPUT_FILE = "skidrow.json"
OUTPUT_FILE = "skidrow_cleaned.json"

with open(INPUT_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

data["downloads"] = [d for d in data["downloads"] if d.get("uris")]

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.write('{\n')
    f.write(f'  "name": {json.dumps(data["name"], ensure_ascii=False)},\n')
    f.write('  "downloads": [\n')

    for i, d in enumerate(data["downloads"]):
        line = json.dumps(d, ensure_ascii=False, separators=(',', ':'))
        sep = ',' if i < len(data["downloads"]) - 1 else ''
        f.write(f'    {line}{sep}\n')

    f.write('  ]\n')
    f.write('}\n')
