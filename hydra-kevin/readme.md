This is kevinj93's / GrimReaper complete collection containing scene and gog release hosted on 1fichier. The JSON files are in a format suitable for use with Hydra.

# Description

**Combined**
Combine all the sections below into a single .json file.

**Scene release (31k+ games)**
The ultimate goal of this project is to gather every Scene Release possible of PC games into a single, easily accessible location.
Made by kevinj93

Stats:
Total Releases: 34k+
Size: 100 TB+

► Last Updated
19-09-2025

► Format
Single RAR archive per release

► Contents
After unpacking, you will get the original Scene Release, in its original format

► Archive Password
kevinj93

**Old Scene release (12k+ games)**
Older Scene Releases (1998-2012)
Made by kevinj93 thanks to GrimReaper

► Last Updated
19-09-2025

► Format
Single RAR archive per release

► Contents
After unpacking, you will get the original Scene Release, in its original format

► Archive Password
kevinj93

**Non-standard format Scene Releases (3k+ games)**
These releases are in non standard format and can't be checked for authenticity.
Made by kevinj93

**GOG (5k+ games)**
GOG Games Complete Collection (Windows, ENG)
Made by kevinj93

► Archive structure
- Game
- DLC (If there's any)
- Goodies (If there's any)

► Last Updated
19-09-2025

► Filename format
GOG slug name + GOG version + date last updated/uploaded

► Password (for encrypted archives)
kevinj93 (some game archives are encrypted due to false positive virus warning on 1fichier)

► Donation
If you appreciate my collection (message written by kevinj93) wand have a few cents to spare,
please consider donating via:
BTC
`bc1qj72l9jsya7c73ugncx20jzxz8ppsmdw2mrs806`
The donations will be used towards extending 1fichier subscription. Any amount is appreciated.
(Donations are for kevinj93, who created this huge collection, not for me,
who only made the GitHub repository and adapted it for Hydra.)

# Code
Kevinj93 provides us with his 1fichiers links in the 1fichier dir, with each folder labeled by letter.
`create_json.py` uses the list of 1fichier dir links to create an initial JSON file `json_to_normalize.json` with the information from 1fichier.

Then, with `normalizer.py`, you can convert this file into a JSON file that can be used by Hydra.

Once you have your various normalized JSON files that can be used by Hydra (`scene.json`, `old_scene.json`, `non_standard.json`, `gog.json`), you can combine them into a single JSON file `combined.json` with `merged.py`.
