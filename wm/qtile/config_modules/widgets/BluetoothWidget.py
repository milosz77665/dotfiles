from libqtile.widget import base
from libqtile.lazy import lazy
from qtile_extras.widget.mixins import TooltipMixin

from ..variables import (
    FAST_UPDATE_INTERVAL,
    BLUETOOTH_APP,
    TOOLTIP_DEFAULTS,
)
from ..services.BluetoothService import bt_service
from ..services.AirplaneModeService import airplane_mode_service


class BluetoothWidget(base.ThreadPoolText, TooltipMixin):
    def __init__(self, **config):
        super().__init__("", **config)
        TooltipMixin.__init__(self, **config)
        self.add_defaults(TooltipMixin.defaults)
        self.add_defaults(TOOLTIP_DEFAULTS)
        self.update_interval = FAST_UPDATE_INTERVAL
        self.mouse_callbacks = {"Button1": lazy.spawn(BLUETOOTH_APP)}
        self.is_enabled = False

    def poll(self):
        self.is_enabled = bt_service.get_status()

        if self.is_enabled:
            output_text = ""
            connected_devices = bt_service.get_connected_devices()
            if len(connected_devices) > 0:
                for device_info in connected_devices.values():
                    self.tooltip_text = f"Device: {device_info["name"]}"
                    output_text = f"󰂱 {device_info["battery"]}%{f" {output_text}" if len(output_text)>0 else ""}"
            else:
                self.tooltip_text = f"No Device Connected"
                output_text = "󰂯"
            return output_text
        else:
            if airplane_mode_service.get_status():
                return ""
            else:
                self.tooltip_text = f"Turned off"
                return "󰂲"
