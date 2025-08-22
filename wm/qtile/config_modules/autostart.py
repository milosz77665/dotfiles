from libqtile import hook
import os
import subprocess
from libqtile.log_utils import logger

from .variables import DEFAULT_WALLPAPER_PATH, TOUCHPAD_NAME
from .utils.touchpad import get_touchpad_id


@hook.subscribe.startup_once
def autostart():
    touchpad_id = get_touchpad_id(TOUCHPAD_NAME)

    if touchpad_id:
        # Enable touchpad tapping
        subprocess.Popen(
            ["xinput", "set-prop", touchpad_id, "libinput Tapping Enabled", "1"]
        )

        # Disable mouse middle button
        subprocess.Popen(
            ["xinput", "set-button-map", touchpad_id, "1", "0", "3", "4", "5", "6", "7"]
        )
    else:
        logger.error(
            f"Nie znaleziono touchpada o nazwie zawierającej: '{TOUCHPAD_NAME}'"
        )

    # Notification Deamon
    subprocess.Popen(["dunst"])

    # Networks
    # subprocess.Popen(["nm-applet"])

    # Bluetooth
    # subprocess.Popen(["blueman-applet"])

    # Policy Agent
    subprocess.Popen(["/usr/lib/policykit-1-gnome/polkit-gnome-authentication-agent-1"])

    # Wallpaper
    if os.path.exists(DEFAULT_WALLPAPER_PATH):
        if os.environ.get("XDG_SESSION_TYPE") == "wayland":
            subprocess.Popen(["swaybg", "-i", DEFAULT_WALLPAPER_PATH])
        else:
            subprocess.Popen(["feh", "--bg-fill", DEFAULT_WALLPAPER_PATH])

    # Pywal
    subprocess.Popen(["wal", "-i", DEFAULT_WALLPAPER_PATH])

    # Picom
    if os.environ.get("XDG_SESSION_TYPE") != "wayland":
        subprocess.Popen(["picom", "-b"])

    # Screensaver
    subprocess.Popen(["xscreensaver", "-no-splash"])
