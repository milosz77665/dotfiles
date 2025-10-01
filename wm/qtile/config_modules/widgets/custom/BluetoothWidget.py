from libqtile.widget import base
from libqtile.lazy import lazy
from qtile_extras.widget.mixins import TooltipMixin

from ...variables import (
    FAST_UPDATE_INTERVAL,
    BLUETOOTH_APP,
    TOOLTIP_DEFAULTS,
)
from .services.BluetoothService import BluetoothService


class BluetoothWidget(base.ThreadPoolText, TooltipMixin):
    def __init__(self, **config):
        super().__init__("", **config)
        TooltipMixin.__init__(self, **config)
        self.add_defaults(TooltipMixin.defaults)
        self.add_defaults(TOOLTIP_DEFAULTS)
        self.update_interval = FAST_UPDATE_INTERVAL
        self.bt_service = BluetoothService()
        self.mouse_callbacks = {
            "Button1": lazy.spawn(BLUETOOTH_APP),
            "Button3": lazy.function(lambda qtile: self.bt_service.toggle_state(qtile)),
        }
        self.is_enabled = False
        self.icon_map = [
            (100, "󰥈"),
            (90, "󰥆"),
            (80, "󰥅"),
            (70, "󰥄"),
            (60, "󰥃"),
            (50, "󰥂"),
            (40, "󰥁"),
            (30, "󰥀"),
            (20, "󰤿"),
            (10, "󰤾"),
        ]

    def poll(self):
        self.is_enabled = self.bt_service.get_status()

        if self.is_enabled:
            output_text = ""
            connected_devices = self.bt_service.get_connected_devices()
            if len(connected_devices) > 0:
                for device_info in connected_devices.values():
                    self.tooltip_text = f"Device: {device_info["name"]}"
                    output_text = f"󰂱 {device_info["battery"]}%{f" {output_text}" if len(output_text)>0 else ""}"
            else:
                self.tooltip_text = f"No Device Connected"
                output_text = "󰂯"
            return output_text
        else:
            self.tooltip_text = f"Turned off"
            return "󰂲"
