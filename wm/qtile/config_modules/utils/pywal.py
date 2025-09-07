import json
import os

FALLBACK_COLORS = [
    {
        "color0": "#fff",
        "color1": "#fff",
        "color2": "#fff",
        "color3": "#fff",
        "color4": "#fff",
        "color5": "#fff",
        "color6": "#fff",
        "color7": "#fff",
        "color8": "#fff",
        "color9": "#fff",
        "color10": "#fff",
        "color11": "#fff",
        "color12": "#fff",
        "color13": "#fff",
        "color14": "#fff",
        "color15": "#000",
    },
    {
        "foreground": "#fff",
        "background": "#000",
    },
]


def load_pywal_colors():
    home = os.path.expanduser("~")
    wal_cache_dir = os.path.join(home, ".cache", "wal")
    colors_json_path = os.path.join(wal_cache_dir, "colors.json")

    if os.path.exists(colors_json_path):
        with open(colors_json_path, "r") as f:
            colors_data = json.load(f)
        if colors_data["colors"] != None and colors_data["special"] != None:
            return colors_data["colors"], colors_data["special"]
    return FALLBACK_COLORS
