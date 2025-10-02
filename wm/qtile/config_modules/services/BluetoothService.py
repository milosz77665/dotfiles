import re
from libqtile.log_utils import logger
import subprocess


class BluetoothService:
    def get_status(self):
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

    def get_connected_devices(self):
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

    def get_discoverable_devices(self):
        discoverable_devices = []
        try:
            output = subprocess.check_output(
                "hcitool scan",
                shell=True,
                text=True,
                stderr=subprocess.PIPE,
            ).strip()

            device_lines = output.splitlines()[1:]

            for line in device_lines:
                match = re.search(
                    r"^\s*(\w{2}:\w{2}:\w{2}:\w{2}:\w{2}:\w{2})\s*(.*)$", line
                )
                if match:
                    mac, name = match.groups()

                    info_output = subprocess.getoutput(f"bluetoothctl info {mac}")

                    connected_match = re.search(r"Connected: (.+)", info_output)
                    connected = (
                        connected_match.group(1).strip() == "yes"
                        if connected_match
                        else False
                    )

                    paired_match = re.search(r"Paired: (.+)", info_output)
                    paired = (
                        paired_match.group(1).strip() == "yes"
                        if paired_match
                        else False
                    )

                    discoverable_devices.append(
                        {
                            "MAC": mac,
                            "name": name.strip(),
                            "connected": connected,
                            "paired": paired,
                        }
                    )

        except subprocess.CalledProcessError as e:
            logger.error(
                f"Error using hcitool scan (maybe missing hcitool or permissions): {e.stderr}"
            )
        except Exception as e:
            logger.error(
                f"Unexpected error getting discoverable Bluetooth devices: {e}"
            )

        return discoverable_devices

    def get_paired_devices(self):
        paired_devices = []
        try:
            devices_output = subprocess.check_output(
                "bluetoothctl devices Paired",
                shell=True,
                text=True,
                stderr=subprocess.PIPE,
            ).strip()

            device_lines = devices_output.splitlines()

            for line in device_lines:
                if line.startswith("Device"):
                    match = re.search(
                        r"Device (\w{2}:\w{2}:\w{2}:\w{2}:\w{2}:\w{2}) (.+)", line
                    )
                    if match:
                        mac, name = match.groups()

                        info_output = subprocess.getoutput(f"bluetoothctl info {mac}")

                        connected_match = re.search(r"Connected: (.+)", info_output)
                        connected = (
                            connected_match.group(1).strip() == "yes"
                            if connected_match
                            else False
                        )

                        battery_match = re.search(
                            r"Battery Percentage: 0x[0-9a-fA-F]+ \((\d+)\)", info_output
                        )
                        battery_percentage = (
                            battery_match.group(1).strip() if battery_match else None
                        )

                        paired_devices.append(
                            {
                                "MAC": mac,
                                "name": name.strip(),
                                "connected": connected,
                                "battery": battery_percentage,
                            }
                        )

        except subprocess.CalledProcessError as e:
            logger.warning(f"Error getting paired Bluetooth devices: {e.stderr}")
        except Exception as e:
            logger.error(f"Unexpected error getting paired Bluetooth devices: {e}")

        return paired_devices

    def connect_device(self, mac_address):
        try:
            logger.info(f"Attempting to connect to {mac_address}...")

            result = subprocess.run(
                f"bluetoothctl connect {mac_address}",
                shell=True,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=15,
            )

            if "successful" in result.stdout or "Already Connected" in result.stdout:
                logger.info(f"Successfully connected to {mac_address}.")
                return True, "Connection successful."

            error_output = result.stderr.strip() or result.stdout.strip()

            return False, f"Connection error: {error_output}"

        except subprocess.TimeoutExpired:
            logger.error(f"Connection attempt to {mac_address} timed out.")
            return False, "Connection attempt timed out."
        except subprocess.CalledProcessError as e:
            error_message = e.stderr.strip() or e.stdout.strip()
            logger.error(f"Error connecting to {mac_address}: {error_message}")
            return False, f"System error during connection: {error_message}"
        except Exception as e:
            logger.error(f"Unexpected error during connection: {e}")
            return False, "An unexpected error occurred."

    def disconnect_device(self, mac_address):
        try:
            logger.info(f"Attempting to disconnect from {mac_address}...")

            result = subprocess.run(
                f"bluetoothctl disconnect {mac_address}",
                shell=True,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=10,
            )

            if "successful" in result.stdout or "not connected" in result.stdout:
                logger.info(f"Successfully disconnected from {mac_address}.")
                return True, "Disconnection successful."

            error_output = result.stderr.strip() or result.stdout.strip()

            return False, f"Disconnection error: {error_output}"

        except subprocess.TimeoutExpired:
            logger.error(f"Disconnection attempt from {mac_address} timed out.")
            return False, "Disconnection attempt timed out."
        except subprocess.CalledProcessError as e:
            error_message = e.stderr.strip() or e.stdout.strip()
            logger.error(f"Error disconnecting from {mac_address}: {error_message}")
            return False, f"System error during disconnection: {error_message}"
        except Exception as e:
            logger.error(f"Unexpected error during disconnection: {e}")
            return False, "An unexpected error occurred."

    def toggle_state(self, qtile):
        status = self.get_status()
        if status is True:
            qtile.spawn("bluetoothctl power off")
        else:
            qtile.spawn("bluetoothctl power on")


bt_service = BluetoothService()
