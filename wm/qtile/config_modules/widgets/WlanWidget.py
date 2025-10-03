from libqtile.widget import base
from libqtile.lazy import lazy
from qtile_extras.widget.mixins import TooltipMixin

from ..variables import (
    FAST_UPDATE_INTERVAL,
    WLAN_INTERFACE,
    WLAN_APP,
    TOOLTIP_DEFAULTS,
)
from ..services.WlanService import WlanService


class WlanWidget(base.ThreadPoolText, TooltipMixin):
    def __init__(self, **config):
        super().__init__("", **config)
        TooltipMixin.__init__(self, **config)
        self.add_defaults(TooltipMixin.defaults)
        self.add_defaults(TOOLTIP_DEFAULTS)
        self.interface = WLAN_INTERFACE
        self.update_interval = FAST_UPDATE_INTERVAL
        self.wlan_service = WlanService()
        self.mouse_callbacks = {
            "Button1": lazy.spawn(WLAN_APP),
            "Button3": lazy.function(
                lambda qtile: self.wlan_service.toggle_state(qtile)
            ),
        }
        self.is_enabled = False
        self.icon_map = [
            (90, "󰤨"),
            (70, "󰤥"),
            (40, "󰤢"),
            (1, "󰤟"),
            (0, "󰤯"),
        ]

    def poll(self):
        self.is_enabled = self.wlan_service.get_status()

        if self.is_enabled:
            essid = self.wlan_service.get_ssid()
            ip_address = self.wlan_service.get_ip_address()
            signal = self.wlan_service.get_signal_strength()
            icon = next(icon for level, icon in self.icon_map if signal >= level)

            self.tooltip_text = (
                f"SSID: {essid} IP: {ip_address}" if len(essid) > 0 else "Disconnected"
            )
            return f"{icon}"
        else:
            self.tooltip_text = "Turned off"
            return f"󰤭"
