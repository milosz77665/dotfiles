from libqtile.widget import base
from libqtile.lazy import lazy
from qtile_extras.widget.mixins import TooltipMixin

from ..variables import (
    FAST_UPDATE_INTERVAL,
    WLAN_INTERFACE,
    WLAN_APP,
    TOOLTIP_DEFAULTS,
)
from ..services.WlanService import wlan_service
from ..services.AirplaneModeService import airplane_mode_service


class WlanWidget(base.ThreadPoolText, TooltipMixin):
    def __init__(self, **config):
        super().__init__("", **config)
        TooltipMixin.__init__(self, **config)
        self.add_defaults(TooltipMixin.defaults)
        self.add_defaults(TOOLTIP_DEFAULTS)
        self.interface = WLAN_INTERFACE
        self.update_interval = FAST_UPDATE_INTERVAL
        self.mouse_callbacks = {"Button1": lazy.spawn(WLAN_APP)}
        self.is_enabled = False
        self.icon_map = [
            (90, "󰤨"),
            (70, "󰤥"),
            (40, "󰤢"),
            (1, "󰤟"),
            (0, "󰤯"),
        ]

    def poll(self):
        self.is_enabled = wlan_service.get_status()

        if self.is_enabled:
            essid = wlan_service.get_ssid()
            ip_address = wlan_service.get_ip_address()
            signal = wlan_service.get_signal_strength()
            icon = next(icon for level, icon in self.icon_map if signal >= level)

            self.tooltip_text = (
                f"SSID: {essid} IP: {ip_address}" if essid else "Disconnected"
            )
            return f"{icon}"
        else:
            if airplane_mode_service.get_status():
                self.tooltip_text = "Airplane mode is active"
                return "󰀝"
            else:
                self.tooltip_text = "Turned off"
                return f"󰤭"
