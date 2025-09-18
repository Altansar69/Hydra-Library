This is a scrap from TorrentLeech's PC video games dated 14-09-2025 in the form of a json compatible with [Hydra](https://github.com/hydralauncher/hydra). It contains approximately 53,000 games.
It contains the various scripts needed to do this. 
`torrents_magnets_without_trackers.json` contains a list of games with their magnet links but cannot be used because it does not contain the tracker link. Since TorrentLeech is a private tracker, the tracker link contains a private passkey. To obtain a usable JSON file, please follow [the steps below](#want-usable-json-for-hydra). 

# Want usable .json for hydra:
1 - Go into `add_trackers.py` and add your TorrentLeech passkey (line 3). You can find your passkey on [TorrentLeech settings](https://www.torrentleech.org/profile/Altansar/view).
2 - Run the program and it will create `usable_json_with_magnets_and_trackers.json`, which you can use. Keep in mind that this JSON file contains your passkey, which is private. Do not share it. 

# Want scrap the website yourself:
1 - Scrap the website with `hydra-tl.py`. It will give you `torrents.json`.
2 - Converts torrent link to magnet link with `convert_TL_link_to_magnet.py`. It will give you `usable_json_with_magnets_and_trackers.json`.
3 - `usable_json_with_magnets_and_trackers.json` is a usable JSON file, but it contains your passkey, which is private. If you intend to use it personally, that's fine. If you intend to share it, continue with the instructions.
4 - Remove trackers from magnets using `remove_trackers.py`. It will give you `torrents_magnets_without_trackers.json`.
5 - The resulting JSON is not usable, but it can be shared safely. You can send the [tutorial to make it usable](#want-usable-json-for-hydra) for the people you share it with.
