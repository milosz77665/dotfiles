import subprocess
from libqtile.log_utils import logger

from ..variables import (
    WLAN_INTERFACE,
)


class WlanService:
    def __init__(self, interface=WLAN_INTERFACE):
        self.interface = interface

    def get_status(self):
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
            return False
        except Exception as e:
            logger.error(f"Unexpected error checking Wi-Fi status: {e}")
            return False

    def get_ssid(self):
        try:
            output = subprocess.check_output(
                f"nmcli -t -f active,ssid dev wifi list | grep -E '^yes|^tak' | cut -d':' -f2",
                shell=True,
                text=True,
                stderr=subprocess.PIPE,
            ).strip()
            return output if output else None
        except subprocess.CalledProcessError:
            return None
        except Exception as e:
            logger.error(f"Unexpected error getting SSID: {e}")
            return None

    def get_ip_address(self):
        try:
            output = subprocess.check_output(
                f"ip -4 addr show {self.interface}"
                + "| grep -oP '(?<=inet\s)\d+(\.\d+){3}'",
                shell=True,
                text=True,
                stderr=subprocess.PIPE,
            ).strip()
            return output if output else None
        except subprocess.CalledProcessError:
            return None
        except Exception as e:
            logger.error(f"Unexpected error getting IP address: {e}")
            return None

    def get_signal_strength(self):
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

    def get_available_networks(self):
        networks = []
        try:
            output = subprocess.check_output(
                f"nmcli -t -f ssid,signal,security dev wifi list --rescan yes",
                shell=True,
                text=True,
                stderr=subprocess.PIPE,
            ).strip()

            seen_ssids = set()
            for line in output.splitlines():
                if line.strip():
                    parts = line.split(":")
                    if len(parts) >= 3:
                        ssid = parts[0].strip()
                        signal = parts[1].strip()
                        security = parts[2].strip()

                        if ssid not in seen_ssids:
                            networks.append(
                                {
                                    "ssid": ssid,
                                    "signal": int(signal) if signal.isdigit() else 0,
                                    "security": security if security else "None",
                                }
                            )
                            seen_ssids.add(ssid)
        except subprocess.CalledProcessError as e:
            logger.warning(f"Error listing Wi-Fi networks: {e.stderr}")
        except Exception as e:
            logger.error(f"Unexpected error listing Wi-Fi networks: {e}")

        return networks

    def connect_to_network(self, ssid, password=None):
        try:
            command = f'nmcli dev wifi connect "{ssid}"'
            if password:
                command += f' password "{password}"'

            result = subprocess.run(
                command,
                shell=True,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=20,
            )

            if "successfully activated" in result.stdout:
                logger.info(f"Successfully connected to {ssid}.")
                return True, "Connection successful."

            error_output = result.stderr.strip() or result.stdout.strip()
            return False, f"Connection failed: {error_output}"

        except subprocess.TimeoutExpired:
            logger.error(f"Connection attempt to {ssid} timed out.")
            return False, "Connection attempt timed out."
        except subprocess.CalledProcessError as e:
            error_message = e.stderr.strip() or e.stdout.strip()
            logger.error(f"Error connecting to {ssid}: {error_message}")
            return False, f"System error during connection: {error_message}"
        except Exception as e:
            logger.error(f"Unexpected error during connection: {e}")
            return False, "An unexpected error occurred."

    def disconnect_from_network(self):
        try:
            # Find the active connection name
            active_connection = subprocess.check_output(
                "nmcli -t -f active,name connection show --active | grep '^yes' | cut -d':' -f2",
                shell=True,
                text=True,
                stderr=subprocess.PIPE,
            ).strip()

            if not active_connection:
                return False, "No active connection found to disconnect."

            # Disconnect using the connection name
            result = subprocess.run(
                f'nmcli connection down "{active_connection}"',
                shell=True,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=10,
            )

            if "successfully deactivated" in result.stdout:
                logger.info(f"Successfully disconnected from {active_connection}.")
                return True, "Disconnection successful."

            error_output = result.stderr.strip() or result.stdout.strip()
            return False, f"Disconnection failed: {error_output}"

        except subprocess.TimeoutExpired:
            logger.error("Disconnection attempt timed out.")
            return False, "Disconnection attempt timed out."
        except subprocess.CalledProcessError as e:
            error_message = e.stderr.strip() or e.stdout.strip()
            logger.error(f"Error disconnecting: {error_message}")
            return False, f"System error during disconnection: {error_message}"
        except Exception as e:
            logger.error(f"Unexpected error during disconnection: {e}")
            return False, "An unexpected error occurred."

    def toggle_state(self, qtile):
        status = self.get_status()
        if status:
            qtile.spawn("nmcli radio wifi off")
        else:
            qtile.spawn("nmcli radio wifi on")


wlan_service = WlanService()
