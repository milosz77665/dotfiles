from libqtile.widget import base
from libqtile.lazy import lazy
from qtile_extras.widget.mixins import TooltipMixin
import subprocess
from libqtile.log_utils import logger

from ...variables import (
    FAST_UPDATE_INTERVAL,
    WLAN_INTERFACE,
    WLAN_APP,
    WLAN_TURN_ON,
    WLAN_TURN_OFF,
    TOOLTIP_DEFAULTS,
)


class WlanWidget(base.ThreadPoolText, TooltipMixin):
    def __init__(self, **config):
        super().__init__("", **config)
        TooltipMixin.__init__(self, **config)
        self.add_defaults(TooltipMixin.defaults)
        self.add_defaults(TOOLTIP_DEFAULTS)
        self.interface = WLAN_INTERFACE
        self.update_interval = FAST_UPDATE_INTERVAL
        self.mouse_callbacks = {
            "Button1": lazy.spawn(WLAN_APP),
            "Button3": lazy.function(self._toggle_wifi_state),
        }
        self.is_enabled = False

    def _get_wifi_status(self):
        try:
            output = subprocess.check_output(
                f"nmcli radio wifi",
                shell=True,
                text=True,
                stderr=subprocess.PIPE,
            ).strip()
            return output.lower() == "enabled"
        except subprocess.CalledProcessError as e:
            logger.error(f"Error checking Wi-Fi status: {e.stderr}")
            return "None"
        except Exception as e:
            logger.error(f"Unexpected error checking Wi-Fi status: {e}")
            return None

    def _get_ssid(self):
        try:
            output = subprocess.check_output(
                f"nmcli -t -f active,ssid dev wifi list | grep '^tak' | cut -d':' -f2",
                shell=True,
                text=True,
                stderr=subprocess.PIPE,
            ).strip()
            return output if output else ""
        except subprocess.CalledProcessError:
            return ""
        except Exception as e:
            logger.error(f"Unexpected error getting SSID: {e}")
            return ""

    def _get_signal_strength(self):
        try:
            output = subprocess.check_output(
                f"nmcli -t -f signal dev wifi list ifname {self.interface} | head -n 1",
                shell=True,
                text=True,
                stderr=subprocess.PIPE,
            ).strip()
            if output.isdigit():
                return int(output)
            return 0
        except Exception as e:
            logger.error(f"Error reading signal strength: {e}")
            return 0

    def _get_wifi_icon(self, strength):
        if strength == 0:
            return " 󰤯 "
        elif strength < 40:
            return " 󰤟 "
        elif strength < 70:
            return " 󰤢 "
        elif strength < 90:
            return " 󰤥 "
        else:
            return " 󰤨 "

    def poll(self):
        self.is_enabled = self._get_wifi_status()

        if self.is_enabled:
            essid = self._get_ssid()
            signal = self._get_signal_strength()
            icon = self._get_wifi_icon(signal)

            self.tooltip_text = f"SSID: {essid}" if len(essid) > 0 else "Disconnected"
            return f"{icon}"
        else:
            self.tooltip_text = "Turned off"
            return f"󰤭"

    def _toggle_wifi_state(self, qtile):
        status = self._get_wifi_status()
        if status:
            qtile.spawn(WLAN_TURN_OFF)
        else:
            qtile.spawn(WLAN_TURN_ON)
