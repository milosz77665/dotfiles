import subprocess
from libqtile.log_utils import logger


class BatteryService:
    def _get_acpi_output(self):
        try:
            output = subprocess.check_output(["acpi", "-b"]).decode("utf-8")
            if not output:
                logger.error("BatteryService: No ACPI output, possibly no battery.")
                return None
            return output.strip().splitlines()[0]
        except subprocess.CalledProcessError:
            logger.error("BatteryService: 'acpi' command not found or failed.")
            return None
        except Exception as e:
            logger.error(f"BatteryService: Unexpected error getting ACPI status: {e}")
            return None

    def get_status(self):
        status_line = self._get_acpi_output()
        if status_line:
            try:
                status = status_line.split(": ")[1].split(", ")[0]
                return status
            except IndexError:
                return "Unknown"
        return "N/A"

    def get_percent(self):
        status_line = self._get_acpi_output()
        if status_line:
            try:
                percent_str = status_line.split(", ")[1].replace("%", "")
                return int(percent_str)
            except (IndexError, ValueError):
                return 0
        return 0

    def get_time_remaining(self):
        status_line = self._get_acpi_output()
        if status_line:
            try:
                parts = status_line.split(", ")
                if len(parts) > 2:
                    time_part = parts[2].split()[0][:-3:]
                    return time_part
                return ""
            except IndexError:
                return ""
        return ""

    def get_capacity(self):
        try:
            output = subprocess.check_output(["acpi", "-V"]).decode("utf-8")
            if not output:
                return "N/A"

            status_line = output.strip().splitlines()[1]
            parts = status_line.split("= ")

            capacity = parts[-1].strip()
            return capacity

        except subprocess.CalledProcessError:
            return "N/A"
        except Exception as e:
            logger.error(f"BatteryService: Error getting capacity: {e}")
            return "N/A"

    def is_charging(self):
        return self.get_status() == "Charging"


battery_service = BatteryService()
