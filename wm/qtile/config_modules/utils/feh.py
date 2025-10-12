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

    # set_sddm_wallpaper(selected)

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


def set_sddm_wallpaper(wallpaper_path):
    wp = Path(wallpaper_path).resolve()

    lines = SDDM_CONFIG_FILE.read_text().splitlines()
    new_lines = []
    replaced = False

    for line in lines:
        stripped_line = line.strip()
        if stripped_line.startswith("background ="):
            indent = line[: line.find(stripped_line)]
            new_lines.append(f"{indent}background = {wp}")
            replaced = True
        else:
            new_lines.append(line)

    if not replaced:
        new_lines.append(f"background = {wp}")

    SDDM_CONFIG_FILE.write_text("\n".join(new_lines) + "\n")


@lazy.function
def change_wallpaper(qtile):
    threading.Thread(target=_change_wallpaper_background, daemon=True).start()
