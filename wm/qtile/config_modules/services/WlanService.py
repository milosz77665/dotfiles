import re
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
                ["nmcli", "radio", "wifi"],
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
                ["nmcli", "-t", "-f", "active,ssid", "dev", "wifi", "list"],
                text=True,
                stderr=subprocess.PIPE,
            ).strip()
            ssid = None
            for line in output.splitlines():
                if not line:
                    continue
                parts = line.split(":", 1)
                if parts and parts[0] in ("yes", "tak", "1"):
                    ssid = parts[1] if len(parts) > 1 else None
                    break
            return ssid
        except subprocess.CalledProcessError:
            return None
        except Exception as e:
            logger.error(f"Unexpected error getting SSID: {e}")
            return None

    def get_ip_address(self):
        try:
            output = subprocess.check_output(
                ["ip", "-4", "addr", "show", self.interface],
                text=True,
                stderr=subprocess.PIPE,
            ).strip()
            m = re.search(r"inet\s+(\d+(?:\.\d+){3})", output)
            ip_addr = m.group(1) if m else ""
            return ip_addr
        except subprocess.CalledProcessError:
            return None
        except Exception as e:
            logger.error(f"Unexpected error getting IP address: {e}")
            return None

    def get_signal_strength(self):
        try:
            output = subprocess.check_output(
                [
                    "nmcli",
                    "-t",
                    "-f",
                    "signal",
                    "dev",
                    "wifi",
                    "list",
                    "ifname",
                    self.interface,
                ],
                text=True,
                stderr=subprocess.PIPE,
            ).strip()
            first_line = output.splitlines()[0] if output.splitlines() else ""
            signal = 0
            if first_line.strip().isdigit():
                signal = int(first_line.strip())
            return signal
        except Exception as e:
            logger.error(f"Error reading signal strength: {e}")
            return 0

    def get_available_networks(self):
        networks = []
        try:
            output = subprocess.check_output(
                [
                    "nmcli",
                    "-t",
                    "-f",
                    "ssid,signal,security",
                    "dev",
                    "wifi",
                    "list",
                    "--rescan",
                    "yes",
                ],
                text=True,
                stderr=subprocess.PIPE,
            ).strip()
            networks = []
            for line in output.splitlines():
                if not line:
                    continue
                ssid, signal, security = (line.split(":", 2) + [""] * 3)[:3]
                networks.append(
                    {"ssid": ssid, "signal": int(signal), "security": security}
                )

        except subprocess.CalledProcessError as e:
            logger.warning(f"Error listing Wi-Fi networks: {e.stderr}")
        except Exception as e:
            logger.error(f"Unexpected error listing Wi-Fi networks: {e}")

        return networks

    def connect_to_network(self, ssid, password=None):
        try:
            command = ["nmcli", "dev", "wifi", "connect", ssid]
            if password:
                command += ["password", password]

            result = subprocess.run(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=20,
            )

            if "successfully activated" in result.stdout:
                logger.info(f"Successfully connected to {ssid}.")
                return True, "Connection successful."

            if not password and "secrets were required" in result.stderr.lower():
                logger.info(f"Password required for {ssid}.")
                return False, "Password required"

            error_output = result.stderr.strip() or result.stdout.strip()
            logger.warning(f"Connection failed for {ssid}: {error_output}")
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
            active_connection = self.get_ssid()

            if not active_connection:
                return False, "No active Wi-Fi connection found to disconnect."

            result = subprocess.run(
                ["nmcli", "connection", "down", active_connection],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=10,
            )

            if "successfully deactivated" in result.stdout.lower():
                logger.info(f"Successfully disconnected from {active_connection}.")
                return True, "Disconnection successful."

            error_output = result.stderr.strip() or result.stdout.strip()
            return False, f"Disconnection failed: {error_output}"

        except subprocess.TimeoutExpired:
            logger.error("Disconnection attempt timed out.")
            return False, "Disconnection attempt timed out."
        except subprocess.CalledProcessError as e:
            error_message = e.stderr.strip() or e.stdout.strip()
            logger.error(
                f"Error disconnecting from {active_connection}: {error_message}"
            )
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
