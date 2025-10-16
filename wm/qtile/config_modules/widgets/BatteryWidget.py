import subprocess
from libqtile.widget import base
from qtile_extras.widget.mixins import TooltipMixin

from ..variables import FAST_UPDATE_INTERVAL, TOOLTIP_DEFAULTS, ASSETS_PATH
from ..services.BatteryService import battery_service


class BatteryWidget(base.ThreadPoolText, TooltipMixin):
    def __init__(self, **config):
        super().__init__("", **config)
        TooltipMixin.__init__(self, **config)
        self.add_defaults(TooltipMixin.defaults)
        self.add_defaults(TOOLTIP_DEFAULTS)
        self.update_interval = FAST_UPDATE_INTERVAL
        self.low_warning_level = 25
        self.high_warning_level = 81
        self.icon_map = [
            (100, "󰁹"),
            (90, "󰂂"),
            (80, "󰂁"),
            (70, "󰂀"),
            (60, "󰁿"),
            (50, "󰁾"),
            (40, "󰁽"),
            (30, "󰁼"),
            (20, "󰁻"),
            (10, "󰁺"),
            (0, "󰂎"),
        ]

    def poll(self):
        status = battery_service.get_status()
        percent = battery_service.get_percent()
        time = battery_service.get_time_remaining()
        capacity = battery_service.get_capacity()

        if percent <= self.low_warning_level and status != "Charging":
            subprocess.run(
                [
                    "dunstify",
                    "-u",
                    "critical",
                    "-i",
                    ASSETS_PATH + "battery-alert.svg",
                    "Low Battery Level",
                ],
                text=True,
                stderr=subprocess.DEVNULL,
            )
        elif percent >= self.high_warning_level and status == "Charging":
            subprocess.run(
                [
                    "dunstify",
                    "-u",
                    "critical",
                    "-i",
                    ASSETS_PATH + "battery-full.svg",
                    f"Battery is over {self.high_warning_level}%. Unplug charger to save battery health",
                ],
                text=True,
                stderr=subprocess.DEVNULL,
            )

        icon = next(icon for level, icon in self.icon_map if percent >= level)

        if status == "Charging":
            self.tooltip_text = f"Full in: {time}\nCapacity: {capacity}"
            status_icon = ""
        else:
            self.tooltip_text = (
                f"Remaining: {time if len(time)>0 else ''}\nCapacity: {capacity}"
            )
            status_icon = icon

        return f"{status_icon} {percent}%"
