This is a scrap of all the site: [Skidrow & Reloaded](https://www.skidrowreloaded.com/) dated 26-09-2025 in the form of a json compatible with [Hydra](https://github.com/hydralauncher/hydra). It contains approximately 111,000 games.

Only links from these hosts were taken: 1fichier, MEGA, Pixeldrain, MediaFire, Gofile, DataNodes, QIWI and magnet link.

The Python script to scrape the entire site and create the JSON is also available here.


# Invalid JSON
There may be errors in the JSON. In particular, games with no links or `null` sizes. You can test your JSON with `validate_json.bat`. You can either correct it manually or use `remove_empty_uris.py` to delete all lines with no links. It will give you `skidrow_cleaned.json`. For `null` sizes, there are relatively few, so you can correct them manually.
As long as `validate_json.bat` does not tell you that the JSON is valid, it will not be usable.
