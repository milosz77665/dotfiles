from libqtile.widget import base
from libqtile.log_utils import logger
from qtile_extras.widget.mixins import TooltipMixin

import subprocess
from ..variables import FAST_UPDATE_INTERVAL, TOOLTIP_DEFAULTS


class BatteryWidget(base.ThreadPoolText, TooltipMixin):
    def __init__(self, **config):
        super().__init__("", **config)
        TooltipMixin.__init__(self, **config)
        self.add_defaults(TooltipMixin.defaults)
        self.add_defaults(TOOLTIP_DEFAULTS)
        self.update_interval = FAST_UPDATE_INTERVAL
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

    def _get_status_percent_and_time(self):
        try:
            output = subprocess.check_output(["acpi", "-b"]).decode("utf-8")
            if not output:
                logger.error("No Battery")

            status_line = output.strip().splitlines()[0]
            parts = status_line.split(", ")

            status = parts[0].split(": ")[1]  # Charging / Discharging / Full
            percent_str = parts[1].replace("%", "")
            percent = int(percent_str)
            time = parts[2][:5:] if len(parts) > 2 else ""

            return status, percent, time
        except Exception as e:
            logger.error("Battery Error")

    def _get_capacity(self):
        try:
            output = subprocess.check_output(["acpi", "-V"]).decode("utf-8")
            if not output:
                logger.error("No Battery")

            status_line = output.strip().splitlines()[1]
            parts = status_line.split("= ")

            capacity = parts[-1].strip()
            return capacity
        except Exception as e:
            logger.error("Battery Error")

    def poll(self):
        status, percent, time = self._get_status_percent_and_time()
        capacity = self._get_capacity()

        icon = next(icon for level, icon in self.icon_map if percent >= level)

        if status == "Charging":
            self.tooltip_text = f"Full in: {time}\nCapacity: {capacity}"
            status_icon = ""
        else:
            self.tooltip_text = f"Remaining: {time}\nCapacity: {capacity}"
            status_icon = icon

        return f"{status_icon} {percent}%"
