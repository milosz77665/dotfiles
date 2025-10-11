from libqtile.config import Group, Match
import os
from .utils.pywal import load_pywal_colors


# Apps
MOD = "mod4"
TERMINAL = "alacritty"
BROWSER = "brave-browser"
CODE_EDITOR = "code"
TEXT_EDITOR = "gnome-text-editor"
NOTES = "obsidian"

# Widget common variables
WLAN_INTERFACE = "wlo1"  # ifconfig
THERMAL_SENSOR_TAG = "Core 0"
MASTER_CHANNEL = "Master"
MIC_CHANNEL = "Capture"
DISK_APP = "baobab"
WLAN_APP = "nm-connection-editor"
BLUETOOTH_APP = "blueman-manager"
AUDIO_APP = "pavucontrol"
BACKLIGHT_NAME = "intel_backlight"
ASSETS_PATH = os.path.expanduser("~/.dotfiles/wm/qtile/config_modules/assets/")

# Autostart
MONITOR_CONFIG_PATH = os.path.expanduser("~/.screenlayout/monitor_config.sh")

# Groups
GROUPS = [
    Group("1", matches=[Match(wm_class="code")]),
    Group("2", matches=[Match(wm_class="code")]),
    Group("3", matches=[Match(wm_class="Alacritty")]),
    Group(
        "4", matches=[Match(wm_class="obsidian"), Match(wm_class="gnome-text-editor")]
    ),
    Group(
        "5",
        matches=[
            Match(wm_class="brave-browser"),
            Match(wm_class="google-chrome"),
            Match(wm_class="firefox_firefox"),
        ],
    ),
    Group("6", matches=[Match(wm_class="spotify"), Match(wm_class="steam")]),
]

# Wallpaper
DEFAULT_WALLPAPER_PATH = os.path.expanduser("~/wallpapers/mountains.jpg")
WALLPAPER_DIR = os.path.expanduser("~/wallpapers")

# Variables retro
# Window
WINDOWS_MARGIN = 0
WINDOWS_BORDER = 3

# Widgets
BAR_HEIGHT = 25
BAR_MARGIN = [0, 0, 0, 0]
FONT = "Hack Nerd Font"
FONTSIZE = 14
GROUPS_CIRCLES_SIZE = 20
PADDING = 4
GROUPS_PADDING = 6
BACKLIGHT_STEP = 2.0
UPDATE_INTERVAL = 12.0
FAST_UPDATE_INTERVAL = 5.0
# Pill Decoration
PILL_RADIUS = 8
PILL_LINE_WIDTH = 0

# Colors
colors, special_colors = load_pywal_colors()

WINDOW_BORDER_FOCUS_COLOR = colors["color2"]
WINDOW_BORDER_NORMAL_COLOR = special_colors["background"]
BAR_BACKGROUND = special_colors["background"]
BAR_FOREGROUND = special_colors["foreground"]
BLUETOOTH_COLOR = "#0082FC"
PILL_COLOR = colors["color15"]
PILL_LINE_COLOR = "#000"
GROUPS_ACTIVE_COLOR = special_colors["foreground"]
GROUPS_OCCUPIED_COLOR = special_colors["foreground"]
GROUPS_EMPTY_COLOR = special_colors["foreground"]
GROUPS_OTHER_SCREEN_COLOR = special_colors["foreground"]

# Tooltip
TOOLTIP_DEFAULTS = [
    ("tooltip_delay", 0.3, "Time in seconds before tooltip displayed"),
    (
        "tooltip_background",
        special_colors["background"],
        "Background colour for tooltip",
    ),
    (
        "tooltip_color",
        BAR_FOREGROUND,
        "Font colur for tooltop",
    ),
    ("tooltip_font", FONT, "Font family for tooltop"),
    ("tooltip_fontsize", 15, "Font size for tooltop"),
    ("tooltip_padding", 10, "int for all sides or list for [top/bottom, left/right]"),
]


# Variables modern
# # Window
# WINDOWS_MARGIN = 3
# WINDOWS_BORDER = 3

# # Pill Decoration
# PILL_RADIUS = 8
# PILL_LINE_WIDTH = 0

# # Colors
# colors, special_colors = load_pywal_colors()

# WINDOW_BORDER_FOCUS_COLOR = special_colors["foreground"]
# WINDOW_BORDER_NORMAL_COLOR = special_colors["background"]
# BAR_BACKGROUND = "#00000000"
# BAR_FOREGROUND = colors["color0"]
# BLUETOOTH_COLOR = "#0082FC"
# PILL_COLOR = colors["color15"]
# PILL_LINE_COLOR = "#000"
# GROUPS_ACTIVE_COLOR = colors["color14"]
# GROUPS_OCCUPIED_COLOR = colors["color2"]
# GROUPS_EMPTY_COLOR = colors["color0"]
# GROUPS_OTHER_SCREEN_COLOR = colors["color14"]

# # Tooltip
# TOOLTIP_DEFAULTS = [
#     ("tooltip_delay", 0.3, "Time in seconds before tooltip displayed"),
#     (
#         "tooltip_background",
#         PILL_COLOR,
#         "Background colour for tooltip",
#     ),
#     (
#         "tooltip_color",
#         BAR_FOREGROUND,
#         "Font colur for tooltop",
#     ),
#     ("tooltip_font", FONT, "Font family for tooltop"),
#     ("tooltip_fontsize", 18, "Font size for tooltop"),
#     ("tooltip_padding", 15, "int for all sides or list for [top/bottom, left/right]"),
# ]
