from libqtile.lazy import lazy
from qtile_extras import widget
from qtile_extras.popup.templates.mpris2 import DEFAULT_LAYOUT
from qtile_extras.widget import modify
from qtile_extras.widget.groupbox2 import GroupBox2

from ..variables import (
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
    THERMAL_SENSOR_TAG,
)
from .custom.BatteryWidget import BatteryWidget
from .custom.BluetoothWidget import BluetoothWidget
from .custom.WlanWidget import WlanWidget
from .custom.VolumeWidget import VolumeWidget
from .decorations.pill import pill_deco
from .decorations.groups import numbers_rules, circles_rules, retro_numbers_rules


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
            format=" {uf}{m}",
            padding=PADDING + 2,
            visible_on_warn=False,
            update_inteval=UPDATE_INTERVAL,
            mouse_callbacks={"Button1": lazy.spawn(DISK_APP)},
        ),
        widget.ThermalSensor(
            tag_sensor=THERMAL_SENSOR_TAG,
            format=" {temp:.0f}{unit}",
            padding=PADDING + 2,
            update_inteval=UPDATE_INTERVAL,
        ),
        widget.Memory(
            format="󰫗 {MemUsed:.1f}{mm}/{MemTotal:.1f}{mm}",
            padding=PADDING + 2,
            measure_mem="G",
            update_inteval=UPDATE_INTERVAL,
        ),
        widget.Memory(
            format="󰾴 {SwapUsed:.1f}G/{SwapTotal:.1f}G",
            padding=PADDING + 2,
            measure_swap="G",
            update_inteval=UPDATE_INTERVAL,
        ),
        widget.CPU(
            format=" {load_percent}%",
            padding=PADDING + 2,
            update_inteval=UPDATE_INTERVAL,
        ),
        widget.Spacer(),
        GroupBox2(
            padding_x=GROUPS_PADDING,
            rules=retro_numbers_rules,
            markup=True,
        ),
        widget.CurrentLayout(scale=0.6),
        widget.Spacer(),
        (widget.Systray() if is_primary else widget.Spacer(length=0)),
        widget.Mpris2(
            name="music_player",
            popup_layout=DEFAULT_LAYOUT,
            width=100,
            scroll=True,
            scroll_interval=0.1,
            scroll_repeat=True,
            mouse_callbacks={"Button1": lazy.widget["music_player"].toggle_player()},
        ),
        widget.Backlight(
            format=" 󰃚 {percent:" + f"{BACKLIGHT_STEP}" + "%}",
            backlight_name=BACKLIGHT_NAME,
        ),
        modify(BluetoothWidget),
        modify(WlanWidget, padding=PADDING + 5),
        modify(VolumeWidget),
        modify(BatteryWidget),
        widget.Clock(format="%d/%m/%y %H:%M:%S"),
    ]
