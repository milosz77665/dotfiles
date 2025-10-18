from libqtile.lazy import lazy
from qtile_extras import widget
from qtile_extras.widget import modify
from qtile_extras.widget.groupbox2 import GroupBox2

from .variables import (
    FONT,
    FONTSIZE,
    PADDING,
    GROUPS_PADDING,
    DISK_APP,
    UPDATE_INTERVAL,
    BAR_BACKGROUND,
    BAR_FOREGROUND,
    THERMAL_SENSOR_TAG,
)
from .widgets.BatteryWidget import BatteryWidget
from .widgets.BluetoothWidget import BluetoothWidget
from .widgets.WlanWidget import WlanWidget
from .widgets.VolumeWidget import VolumeWidget
from .widgets.MicWidget import MicWidget
from .widgets.NotificationWidget import NotificationWidget
from .popups.CalendarPopup import calendar_popup
from .popups.NotificationPopup import notification_popup
from .decorations.groups import retro_numbers_rules


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
        widget.WidgetBox(
            text_closed="",
            text_open="",
            widgets=[
                widget.Mpris2(
                    name="music_player",
                    width=200,
                    scroll=True,
                    scroll_interval=0.03,
                    scroll_repeat=True,
                ),
            ],
        ),
        (widget.Systray() if is_primary else widget.Spacer(length=0)),
        widget.Spacer(length=10),
        modify(BluetoothWidget),
        modify(WlanWidget, padding=PADDING + 5),
        modify(MicWidget),
        modify(VolumeWidget),
        modify(BatteryWidget),
        modify(
            NotificationWidget,
            mouse_callbacks={
                "Button1": lazy.function(lambda qtile: notification_popup.toggle(qtile))
            },
        ),
        widget.Clock(
            format="%d/%m/%y %H:%M:%S",
            mouse_callbacks={
                "Button1": lazy.function(lambda qtile: calendar_popup.toggle(qtile))
            },
        ),
    ]
