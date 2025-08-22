import re
from libqtile.widget import base
from libqtile.lazy import lazy
from libqtile.log_utils import logger
import subprocess
from qtile_extras.widget.mixins import TooltipMixin

from ...variables import (
    FAST_UPDATE_INTERVAL,
    BLUETOOTH_APP,
    BLUETOOTH_TURN_ON,
    BLUETOOTH_TURN_OFF,
    TOOLTIP_DEFAULTS,
)


class BluetoothWidget(base.ThreadPoolText, TooltipMixin):
    def __init__(self, **config):
        super().__init__("", **config)
        TooltipMixin.__init__(self, **config)
        self.add_defaults(TooltipMixin.defaults)
        self.add_defaults(TOOLTIP_DEFAULTS)
        self.update_interval = FAST_UPDATE_INTERVAL
        self.mouse_callbacks = {
            "Button1": lazy.spawn(BLUETOOTH_APP),
            "Button3": lazy.function(self._toggle_bluetooth_state),
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

    def _get_bluetooth_status(self):
        try:
            output = subprocess.check_output(
                "bluetoothctl show | grep -oP 'Powered: \\K(yes|no)'",
                shell=True,
                text=True,
                stderr=subprocess.PIPE,
            ).strip()
            return output == "yes"
        except subprocess.CalledProcessError as e:
            logger.error(f"Error checking Bluetooth status: {e.stderr}")
            return " ERR"
        except Exception as e:
            logger.error(f"Unexpected error checking Bluetooth status: {e}")
            return " ERR"

    def _get_connected_devices(self):
        connected_devices = {}
        try:
            devices_output = subprocess.check_output(
                "bluetoothctl devices",
                shell=True,
                text=True,
                stderr=subprocess.PIPE,
            ).strip()

            device_macs = re.findall(
                r"Device (\w{2}:\w{2}:\w{2}:\w{2}:\w{2}:\w{2})", devices_output
            )

            for mac in device_macs:
                info_output = subprocess.check_output(
                    f"bluetoothctl info {mac}",
                    shell=True,
                    text=True,
                    stderr=subprocess.PIPE,
                ).strip()

                name_match = re.search(r"Name: (.+)", info_output)
                connected_match = re.search(r"Connected: (.+)", info_output)
                battery_match = re.search(
                    r"Battery Percentage: 0x[0-9a-fA-F]+ \((\d+)\)", info_output
                )

                if connected_match and connected_match.group(1).strip() == "yes":
                    device_name = (
                        name_match.group(1).strip() if name_match else "Unknown Device"
                    )
                    battery_percentage = (
                        battery_match.group(1).strip() if battery_match else "?"
                    )
                    connected_devices[mac] = {
                        "name": device_name,
                        "battery": battery_percentage,
                    }

        except subprocess.CalledProcessError as e:
            logger.warning(f"Error getting Bluetooth devices info: {e.stderr}")
        except Exception as e:
            logger.error(f"Unexpected error getting Bluetooth devices info: {e}")

        return connected_devices

    def poll(self):
        self.is_enabled = self._get_bluetooth_status()

        if self.is_enabled:
            output_text = ""
            connected_devices = self._get_connected_devices()
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

    def _toggle_bluetooth_state(self, qtile):
        status = self._get_bluetooth_status()
        if status is True:
            qtile.spawn(BLUETOOTH_TURN_OFF)
        else:
            qtile.spawn(BLUETOOTH_TURN_ON)
