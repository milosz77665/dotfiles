from libqtile import hook
import os
import subprocess
from libqtile.log_utils import logger

from .variables import DEFAULT_WALLPAPER_PATH, MONITOR_CONFIG_PATH
from .utils.touchpad import configure_touchpad


@hook.subscribe.startup_once
def autostart():
    # Configure Monitors
    if os.path.exists(MONITOR_CONFIG_PATH):
        subprocess.call([MONITOR_CONFIG_PATH])

    # Touchpad configuration
    configure_touchpad()

    # Notification Deamon
    subprocess.Popen(["dunst"])

    # Networks
    # subprocess.Popen(["nm-applet"])

    # Bluetooth
    # subprocess.Popen(["blueman-applet"])

    # Policy Agent
    if os.path.exists("/usr/lib/policykit-1-gnome/polkit-gnome-authentication-agent-1"):
        subprocess.Popen(
            ["/usr/lib/policykit-1-gnome/polkit-gnome-authentication-agent-1"]
        )

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
        subprocess.Popen(["pkill", "picom"])
        subprocess.Popen(["picom", "--backend", "glx", "--vsync", "-b"])

    # Screensaver
    subprocess.Popen(["xscreensaver", "-no-splash"])
