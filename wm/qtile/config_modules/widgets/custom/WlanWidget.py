from libqtile.widget import base
from libqtile.lazy import lazy
from qtile_extras.widget.mixins import TooltipMixin

from ...variables import (
    FAST_UPDATE_INTERVAL,
    WLAN_INTERFACE,
    WLAN_APP,
    TOOLTIP_DEFAULTS,
)
from ...services.WlanService import WlanService


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

    def _get_wifi_icon(self, strength):
        if strength == 0:
            return "󰤯"
        elif strength < 40:
            return "󰤟"
        elif strength < 70:
            return "󰤢"
        elif strength < 90:
            return "󰤥"
        else:
            return "󰤨"

    def poll(self):
        self.is_enabled = self.wlan_service.get_status()

        if self.is_enabled:
            essid = self.wlan_service.get_ssid()
            signal = self.wlan_service.get_signal_strength()
            icon = self._get_wifi_icon(signal)

            self.tooltip_text = f"SSID: {essid}" if len(essid) > 0 else "Disconnected"
            return f"{icon}"
        else:
            self.tooltip_text = "Turned off"
            return f"󰤭"
