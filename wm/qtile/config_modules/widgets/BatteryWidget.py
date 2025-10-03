from libqtile.widget import base
from qtile_extras.widget.mixins import TooltipMixin

from ..variables import FAST_UPDATE_INTERVAL, TOOLTIP_DEFAULTS
from ..services.BatteryService import BatteryService


class BatteryWidget(base.ThreadPoolText, TooltipMixin):
    def __init__(self, **config):
        super().__init__("", **config)
        TooltipMixin.__init__(self, **config)
        self.add_defaults(TooltipMixin.defaults)
        self.add_defaults(TOOLTIP_DEFAULTS)
        self.update_interval = FAST_UPDATE_INTERVAL
        self.battery_service = BatteryService()
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
        status = self.battery_service.get_status()
        percent = self.battery_service.get_percent()
        time = self.battery_service.get_time_remaining()
        capacity = self.battery_service.get_capacity()

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
