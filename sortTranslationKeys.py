import json
from pathlib import Path

matomo_dir = Path("..")
files = sorted(matomo_dir.glob("**/en.json"))
for file in files:
    plugin_json = file.parent.parent / "plugin.json"
    if not plugin_json.exists():
        continue
    with plugin_json.open() as f:
        plugin_data = json.load(f)
        if "authors" not in plugin_data:
            continue
        if plugin_data["authors"][0]["name"] != "Lukas Winkler":
            continue
        if plugin_data["name"] != "DiagnosticsExtended":
            continue
    print(file)

    with file.open("r") as f:
        data = json.load(f)

    with file.open("w") as f:
        json.dump(data, f, indent=4, ensure_ascii=False, sort_keys=True)
        f.write("\n")
