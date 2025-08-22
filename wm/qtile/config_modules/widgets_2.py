# https://codeberg.org/thelinuxfraud/.config/src/branch/main/qtile/config.py

from libqtile import widget, bar
from .variables import (
    FONT,
    FONTSIZE,
    PADDING,
    BACKLIGHT_NAME,
    BACKLIGHT_STEP,
    colors,
    special_colors,
)
import os
from libqtile.lazy import lazy
from qtile_extras.widget.decorations import BorderDecoration
from qtile_extras.widget.decorations import RectDecoration

colors1 = [
    colors["color0"],
    colors["color1"],
    colors["color2"],
    colors["color3"],
    colors["color4"],
    colors["color5"],
    colors["color6"],
    colors["color7"],
    colors["color8"],
    colors["color9"],
    colors["color10"],
    colors["color11"],
    colors["color12"],
    colors["color13"],
    colors["color14"],
]
widget_defaults = dict(
    font=FONT,
    fontsize=FONTSIZE,
    padding=PADDING,
    background=special_colors["background"],
    foreground=special_colors["foreground"],
)
extension_defaults = widget_defaults.copy()

widget_list = [
    widget.Sep(linewidth=1, padding=5, foreground="#4c566a", background="#2e3440"),
    widget.CurrentLayoutIcon(
        padding=4, scale=0.7, foreground="#d8dee9", background="#2e3440"
    ),
    widget.Sep(linewidth=1, padding=5, foreground="#4c566a", background="#2e3440"),
    widget.GroupBox(
        font="RobotoMono Nerd Font Bold",
        fontsize=12,
        margin_y=2,
        margin_x=3,
        padding_y=2,
        padding_x=3,
        borderwidth=0,
        disable_drag=True,
        active="#4c566a",
        inactive="#2e3440",
        rounded=False,
        highlight_method="text",
        this_current_screen_border="#d8dee9",
        foreground="#4c566a",
        background="#2e3440",
    ),
    widget.Sep(linewidth=1, padding=5, foreground="#4c566a", background="#2e3440"),
    widget.Prompt(
        font="RobotoMono Nerd Font",
        fontsize=12,
        background="#2e3440",
        foreground="#d8dee9",
    ),
    widget.WindowName(
        font="RobotoMono Nerd Font Bold",
        fontsize=12,
        foreground="#d8dee9",
        background="#2e3440",
    ),
    widget.Sep(foreground="#4c566a", background="#2e3440", padding=5, linewidth=1),
    widget.Net(
        foreground="#2e3440",
        background="#2e3440",
        font="RobotoMono Nerd Font Bold",
        fontsize=12,
        format="{down} ↓↑ {up}",
        interface="wlan0",
        decorations=[
            RectDecoration(colour="#8fbcbb", padding_y=3, radius=2, filled=True),
        ],
    ),
    widget.Sep(linewidth=1, padding=5, foreground="#4c566a", background="#2e3440"),
    widget.CPU(
        background="#2e3440",
        foreground="#2e3440",
        font="RobotoMono Nerd Font Bold",
        fontsize=12,
        decorations=[
            RectDecoration(colour="#ebcb8b", padding_y=3, radius=2, filled=True),
        ],
    ),
    widget.Sep(linewidth=1, padding=5, foreground="4c566a", background="#2e3440"),
    widget.Memory(
        measure_mem="G",
        foreground="#2e3440",
        background="#2e3440",
        font="RobotoMono Nerd Font Bold",
        fontsize=12,
        decorations=[
            RectDecoration(colour="#88c0d0", padding_y=3, radius=2, filled=True),
        ],
    ),
    widget.Sep(linewidth=1, padding=5, foreground="#4c566a", background="#2e3440"),
    widget.DF(
        visible_on_warn=False,
        background="#2e3440",
        foreground="#2e3440",
        font="RobotoMono Nerd Font Bold",
        fontsize=12,
        decorations=[
            RectDecoration(colour="#a3be8c", padding_y=3, radius=2, filled=True),
        ],
    ),
    widget.Sep(linewidth=1, padding=5, background="#2e3440", foreground="#4c566a"),
    widget.Clock(
        foreground="#2e3440",
        background="#2e3440",
        font="RobotoMono Nerd Font Bold",
        fontsize=12,
        format="%D %H:%M",
        decorations=[
            RectDecoration(colour="#81a1c1", padding_y=3, radius=2, filled=True),
        ],
    ),
    widget.Sep(linewidth=1, padding=5, foreground="#4c566a", background="#2e3440"),
    # widget.UPowerWidget(
    #     background="#2e3440",
    #     border_colour="#d8dee9",
    #     border_critical_colour="#bf616a",
    #     border_charge_colour="#d8dee9",
    #     fill_low="#ebcb8b",
    #     fill_charge="#a3be8c",
    #     fill_critical="#bf616a",
    #     fill_normal="#d8dee9",
    #     percentage_low=0.4,
    #     percentage_critical=0.2,
    #     font="RobotoMono Nerd Font",
    # ),
    widget.StatusNotifier(background="#2e3440", icon_size=20, padding=5),
    # widget.Systray(
    #    background = "#2e3440",
    #    icon_size = 20,
    #    padding = 5,
    #    ),
    widget.Sep(linewidth=1, padding=5, foreground="#4c566a", background="#2e3440"),
    widget.OpenWeather(
        app_key="4cf3731a25d1d1f4e4a00207afd451a2",
        cityid="4997193",
        format="{main_temp}° {icon}",
        metric=False,
        font="RobotoMono Nerd Font Bold",
        fontsize=12,
        background="#2e3440",
        foreground="#d8dee9",
        decorations=[
            RectDecoration(colour="#2e3440", padding_y=3, radius=2, filled=True),
        ],
    ),
    widget.Sep(linewidth=1, padding=5, background="#2e3440", foreground="#4c566a"),
]
