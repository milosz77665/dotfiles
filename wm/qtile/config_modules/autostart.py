from libqtile import hook
import os
import subprocess

from .variables import DEFAULT_WALLPAPER_PATH, MONITOR_CONFIG_PATH
from .utils.touchpad import configure_touchpad


@hook.subscribe.startup_once
def autostart():
    # Configure Monitors
    if os.path.exists(MONITOR_CONFIG_PATH):
        subprocess.call([MONITOR_CONFIG_PATH])

    # Touchpad configuration
    configure_touchpad()

    # Gnome keyring
    subprocess.Popen(
        ["/usr/bin/gnome-keyring-daemon", "--start", "--components=secrets,ssh"]
    )

    # Policy kit
    subprocess.Popen(["lxpolkit"])

    # Wallpaper
    if os.path.exists(DEFAULT_WALLPAPER_PATH):
        if os.environ.get("XDG_SESSION_TYPE") == "wayland":
            subprocess.Popen(["swaybg", "-i", DEFAULT_WALLPAPER_PATH])
        else:
            subprocess.Popen(["feh", "--bg-fill", DEFAULT_WALLPAPER_PATH])

        # Pywal
        wal_process = subprocess.run(["wal", "-i", DEFAULT_WALLPAPER_PATH])

        if wal_process.returncode == 0:
            subprocess.run(["killall", "dunst"])
            subprocess.run(["wal", "-R"])

            # Notification Deamon
            dunst_config_path = os.path.expanduser("~/.cache/wal/dunstrc")
            subprocess.Popen(["dunst", "-conf", dunst_config_path])

    # Picom
    if os.environ.get("XDG_SESSION_TYPE") != "wayland":
        subprocess.Popen(["pkill", "picom"])
        subprocess.Popen(["picom", "--backend", "glx", "--vsync", "-b"])

    # Screensaver
    # subprocess.Popen(["xscreensaver", "-no-splash"])
