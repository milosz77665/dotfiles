from libqtile.config import Group
import os
from .utils.pywal import load_pywal_colors


# Apps
MOD = "mod4"
TERMINAL = "alacritty"
BROWSER = "brave-browser"
CODE_EDITOR = "code"
TEXT_EDITOR = "gnome-text-editor"
NOTES = "joplin"

# Autostart
TOUCHPAD_NAME = "Microsoft Surface Type Cover Touchpad"

# Groups
GROUPS = [Group(i) for i in "1234"]

# Wallpaper
DEFAULT_WALLPAPER_PATH = os.path.expanduser(
    "~/Obrazy/Wallpapers/stars-2179083-1920.jpg"
)
WALLPAPER_DIR = os.path.expanduser("~/Obrazy/Wallpapers")

# Window
WINDOWS_MARGIN = 12
WINDOWS_BORDER = 3

# Widgets
BAR_HEIGHT = 40
BAR_MARGIN = [10, 15, 0, 15]
FONT = "Hack Nerd Font"
FONTSIZE = 18
PADDING = 8
BACKLIGHT_NAME = "intel_backlight"
BACKLIGHT_STEP = 2.0
WLAN_INTERFACE = "wlp1s0"
DISK_APP = "baobab"
WLAN_APP = "nm-connection-editor"
BLUETOOTH_APP = "blueman-manager"
AUDIO_APP = "pavucontrol"
UPDATE_INTERVAL = 12.0
FAST_UPDATE_INTERVAL = 5.0
BLUETOOTH_TURN_ON = "bluetoothctl power on"
BLUETOOTH_TURN_OFF = "bluetoothctl power off"
WLAN_TURN_ON = "nmcli radio wifi on"
WLAN_TURN_OFF = "nmcli radio wifi off"

# Pill Decoration
PILL_RADIUS = 20
PILL_LINE_WIDTH = 0

if os.path.exists(DEFAULT_WALLPAPER_PATH):
    # Colors
    colors, special_colors = load_pywal_colors()
else:
    colors = {
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
    }
    special_colors = {
        "foreground": "#fff",
        "background": "#000",
    }

WINDOW_BORDER_FOCUS_COLOR = special_colors["foreground"]
WINDOW_BORDER_NORMAL_COLOR = special_colors["background"]
BAR_BACKGROUND = "#00000000"
BAR_FOREGROUND = colors["color0"]
BLUETOOTH_COLOR = "#0082FC"
PILL_COLOR = colors["color15"]
PILL_LINE_COLOR = "#000"

# Tooltip
TOOLTIP_DEFAULTS = [
    ("tooltip_delay", 0.3, "Time in seconds before tooltip displayed"),
    (
        "tooltip_background",
        PILL_COLOR,
        "Background colour for tooltip",
    ),
    (
        "tooltip_color",
        BAR_FOREGROUND,
        "Font colur for tooltop",
    ),
    ("tooltip_font", FONT, "Font family for tooltop"),
    ("tooltip_fontsize", 18, "Font size for tooltop"),
    ("tooltip_padding", 15, "int for all sides or list for [top/bottom, left/right]"),
]


# fix
#     def _stop_tooltip(self, x, y):
#         if self._tooltip_timer:
#             self._tooltip_timer.cancel()
#             self._tooltip_timer = None

#         if self._tooltip:
#             self._tooltip.hide()
#             self._tooltip.kill()
#             self._tooltip = None
