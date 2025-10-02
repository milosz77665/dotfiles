from libqtile.lazy import lazy
from qtile_extras import widget
from qtile_extras.popup.templates.mpris2 import DEFAULT_LAYOUT
from qtile_extras.widget import modify
from qtile_extras.widget.groupbox2 import GroupBox2

from .variables import (
    FONT,
    FONTSIZE,
    GROUPS_CIRCLES_SIZE,
    PADDING,
    GROUPS_PADDING,
    DISK_APP,
    UPDATE_INTERVAL,
    BACKLIGHT_NAME,
    BACKLIGHT_STEP,
    BAR_BACKGROUND,
    BAR_FOREGROUND,
)
from .widgets.BatteryWidget import BatteryWidget
from .widgets.BluetoothWidget import BluetoothWidget
from .widgets.WlanWidget import WlanWidget
from .widgets.VolumeWidget import VolumeWidget
from .popups.CalendarPopup import calendar_popup
from .decorations.pill import pill_deco
from .decorations.groups import numbers_rules, circles_rules


widget_defaults = dict(
    font=FONT,
    fontsize=FONTSIZE,
    padding=PADDING,
    background=BAR_BACKGROUND,
    foreground=BAR_FOREGROUND,
)
extension_defaults = widget_defaults.copy()


def get_widget_list(is_primary=False):
    return [
        widget.DF(
            format="  {uf}{m}",
            visible_on_warn=False,
            update_inteval=UPDATE_INTERVAL,
            mouse_callbacks={"Button1": lazy.spawn(DISK_APP)},
            **pill_deco,
        ),
        widget.ThermalSensor(
            format=" {temp:.0f}{unit}", update_inteval=UPDATE_INTERVAL, **pill_deco
        ),
        widget.Memory(
            measure_mem="G",
            update_inteval=UPDATE_INTERVAL,
            format="󰫗  {MemUsed:.1f}{mm}/{MemTotal:.1f}{mm}",
            **pill_deco,
        ),
        widget.Memory(
            measure_swap="G",
            update_inteval=UPDATE_INTERVAL,
            format="󰾴 {SwapUsed:.1f}G/{SwapTotal:.1f}G",
            **pill_deco,
        ),
        widget.CPU(
            format="  {load_percent}%", update_inteval=UPDATE_INTERVAL, **pill_deco
        ),
        widget.Mpris2(
            name="music_player",
            popup_layout=DEFAULT_LAYOUT,
            width=100,
            scroll=True,
            scroll_interval=0.1,
            scroll_repeat=True,
            mouse_callbacks={"Button1": lazy.widget["music_player"].toggle_player()},
            **pill_deco,
        ),
        widget.Spacer(),
        GroupBox2(
            fontsize=GROUPS_CIRCLES_SIZE,
            padding_x=GROUPS_PADDING,
            rules=numbers_rules,
        ),
        widget.CurrentLayout(scale=0.6, **pill_deco),
        widget.Spacer(),
        (widget.Systray() if is_primary else widget.Spacer(length=0)),
        widget.Backlight(
            format="󰃚 {percent:" + f"{BACKLIGHT_STEP}" + "%}",
            backlight_name=BACKLIGHT_NAME,
            **pill_deco,
        ),
        modify(BluetoothWidget, **pill_deco),
        modify(WlanWidget, **pill_deco),
        modify(VolumeWidget, **pill_deco),
        modify(BatteryWidget, **pill_deco),
        widget.Clock(
            format="%d / %m / %y  %H:%M:%S",
            mouse_callbacks={
                "Button1": lazy.function(lambda qtile: calendar_popup.toggle(qtile))
            },
            **pill_deco,
        ),
    ]
