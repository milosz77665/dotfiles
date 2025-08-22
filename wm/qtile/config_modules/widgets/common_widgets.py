from libqtile import widget
from libqtile.lazy import lazy
from qtile_extras import widget as extra_widget
from qtile_extras.popup.templates.mpris2 import DEFAULT_LAYOUT

from ..variables import BACKLIGHT_NAME, BACKLIGHT_STEP, BAR_FOREGROUND, BAR_BACKGROUND


def get_common_music_player():
    return extra_widget.Mpris2(
        name="music_player",
        popup_layout=DEFAULT_LAYOUT,
        width=300,
        scroll=True,
        scroll_interval=0.1,
        scroll_repeat=True,
        mouse_callbacks={"Button1": lazy.widget["music_player"].toggle_player()},
    )


def get_common_systray():
    return widget.Systray()


def get_common_groupbox():
    return widget.GroupBox(
        margin_y=3,
        margin_x=0,
        padding_y=5,
        padding_x=3,
        borderwidth=2,
        active=BAR_FOREGROUND,
        inactive=BAR_FOREGROUND + "80",
        highlight_method="line",
        rounded=True,
        this_current_screen_border=BAR_FOREGROUND,
        this_screen_border=BAR_FOREGROUND,
        other_current_screen_border=BAR_BACKGROUND,
        other_screen_border=BAR_BACKGROUND,
    )


def get_common_backlight():
    return widget.Backlight(
        format="󰃚 {percent:" + f"{BACKLIGHT_STEP}" + "%}",
        backlight_name=BACKLIGHT_NAME,
    )


def get_common_clock():
    return widget.Clock(
        format="%d %b %H:%M",
    )
