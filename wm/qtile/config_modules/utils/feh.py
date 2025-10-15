import os
import random
import subprocess
import threading
from pathlib import Path
from libqtile.lazy import lazy
from libqtile.log_utils import logger

from ..variables import WALLPAPER_DIR, SDDM_CONFIG_FILE


def _change_wallpaper_background():
    wallpapers = [
        os.path.join(WALLPAPER_DIR, f)
        for f in os.listdir(WALLPAPER_DIR)
        if f.lower().endswith((".jpg", ".png"))
    ]

    if not wallpapers:
        logger.error("No wallpapers found")
        return

    selected = random.choice(wallpapers)

    subprocess.Popen(["betterlockscreen", "-u", selected])

    if os.environ.get("XDG_SESSION_TYPE") != "wayland":
        subprocess.Popen(["feh", "--bg-fill", selected])
    else:
        subprocess.Popen(["swaybg", "-i", selected])

    subprocess.run(
        ["wal", "-i", selected],
        env=os.environ.copy(),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    subprocess.run(["qtile", "cmd-obj", "-o", "cmd", "-f", "reload_config"])
    subprocess.run(["killall", "dunst"])
    dunst_config_path = os.path.expanduser("~/.cache/wal/dunstrc")
    subprocess.Popen(["dunst", "-conf", dunst_config_path])

@lazy.function
def change_wallpaper(qtile):
    threading.Thread(target=_change_wallpaper_background, daemon=True).start()
