# https://github.com/JhonatanFerrer/JhoalfercoQtileDotfiles/blob/main/.config/qtile/config.py


import os
import subprocess
from libqtile import qtile
from qtile_extras import widget  # as extrawidgets #Extras
from qtile_extras.widget.decorations import (
    RectDecoration,
)
from .variables import colors

background = "#1a1b26"  # dark purple
foreground = "#a9b1d6"  # "white"
foreground_inactive = "#565f89"  # "dark gray"
foreground2 = background
urgent_color = "#f7768e"  # "red"
color1 = "#bb9af7"  # magenta
color2 = "#ff9e64"  # orange
color3 = "#9ece6a"  # green
color4 = "#2ac3de"  # cyan
color5 = "#7aa2f7"  # blue

widget_defaults = dict(
    font="UbuntuNerdFont",
    fontsize=14,
    padding=3,
    foreground=foreground,
)
extension_defaults = widget_defaults.copy()


widget_list = [
    widget.TextBox("  "),
    widget.GroupBox(
        highlight_method="line",
        active=foreground,
        inactive=foreground_inactive,
        highlight_color=background,
        this_current_screen_border=color1,
        this_screen_border=color5,
        other_current_screen_border=foreground_inactive,
        other_screen_border=foreground_inactive,
        urgent_border=urgent_color,
        urgent_text=urgent_color,
    ),
    widget.WindowName(for_current_screen=True),
    widget.Systray(),
    widget.TextBox(" ", fontsize=40, padding=-14, foreground=color2),
    widget.Volume(
        mute_format="",
        unmute_format="  {volume}%",
        step=5,
        background=color2,
        foreground=foreground2,
    ),
    # widget.Battery(
    #     charge_char="󱊥",
    #     discharge_char="󱊢",
    #     empty_char="󰂎",
    #     full_char="󱊣",
    #     low_percentage=0.1,
    #     low_background=urgent_color,
    #     low_foreground=foreground2,
    #     format='{char} {percent:2.0%}',
    #     update_interval=2,
    #     background=color2,
    #     foreground=foreground2
    # ),
    widget.KeyboardLayout(
        configured_keyboards=["us intl", "es"],
        display_map={"us intl": "   us intl", "es": "   es"},
        background=color2,
        foreground=foreground2,
    ),
    widget.TextBox(
        " ", fontsize=40, padding=-14, background=color2, foreground=color3
    ),
    # widget.Wlan(
    #     format='{essid}',
    #     interface='wlp2s0',
    #     disconnected_message='Desconectado',
    #     ethernet_interface='enp1s0f1',
    #     ethernet_message='󰈀',
    #     background=color3,
    #     foreground=foreground2
    # ),
    widget.Net(
        format="{down:6.2f}{down_suffix:<2} {up:6.2f}{up_suffix:<2}",
        background=color3,
        foreground=foreground2,
    ),
    widget.TextBox(
        " ", fontsize=40, padding=-14, background=color3, foreground=color4
    ),
    widget.CPU(format=" {load_percent}% ", background=color4, foreground=foreground2),
    widget.Memory(
        format=" {MemUsed: .0f}{mm}", background=color4, foreground=foreground2
    ),
    widget.TextBox(
        " ", fontsize=40, padding=-14, background=color4, foreground=color5
    ),
    widget.Clock(format="%a %d/%m %I:%M %p", background=color5, foreground=foreground2),
    widget.TextBox(
        " ", fontsize=40, padding=-14, background=color5, foreground=color1
    ),
    widget.WidgetBox(
        widgets=[
            widget.QuickExit(
                default_text=" 󰍃",
                countdown_format=" {}  ",
                background=color1,
                foreground=foreground2,
            ),
            # widget.TextBox(
            #     " 󰐥",
            #     background=color1,
            #     foreground=foreground2,
            #     mouse_callbacks={"Button1": lazy.spawn(powerMenu)},
            # ),
        ],
        text_closed=" ",
        text_open="  ",
        background=color1,
        foreground=foreground2,
    ),
    widget.TextBox("  ", background=color1),
]
