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
MONITOR_CONFIG = os.path.expanduser("~/.screenlayout/monitor_config.sh")

# Groups
GROUPS = [Group(i) for i in "123456"]

# Wallpaper
DEFAULT_WALLPAPER_PATH = os.path.expanduser("~/wallpapers/mountains.jpg")
WALLPAPER_DIR = os.path.expanduser("~/wallpapers")

# Window
WINDOWS_MARGIN = 8
WINDOWS_BORDER = 2

# Widgets
BAR_HEIGHT = 25
BAR_MARGIN = [5, 10, 0, 10]
FONT = "Hack Nerd Font"
FONTSIZE = 16
GROUPS_CIRCLES_SIZE = 20
PADDING = 12
GROUPS_PADDING = 6
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
PILL_RADIUS = 8
PILL_LINE_WIDTH = 0

# Colors
colors, special_colors = load_pywal_colors()

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
