import json
import os


def load_pywal_colors():
    home = os.path.expanduser("~")
    wal_cache_dir = os.path.join(home, ".cache", "wal")
    colors_json_path = os.path.join(wal_cache_dir, "colors.json")

    if os.path.exists(colors_json_path):
        with open(colors_json_path, "r") as f:
            colors_data = json.load(f)
        return colors_data["colors"], colors_data["special"]
