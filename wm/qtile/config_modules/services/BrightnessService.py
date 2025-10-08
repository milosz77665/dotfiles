import re
import subprocess
from libqtile.log_utils import logger


class BrightnessService:
    def get_brightness(self):
        try:
            output = subprocess.check_output(
                ["brightnessctl", "i"],
                text=True,
                stderr=subprocess.PIPE,
            )
            m = re.search(r"\((\d+)%\)", output)
            brightness_percent = int(m.group(1)) if m else None

            return brightness_percent

        except subprocess.CalledProcessError as e:
            logger.error(
                f"BrightnessService: Error getting brightness (brightnessctl): {e.stderr.strip()}"
            )
            return 0
        except Exception as e:
            logger.error(f"BrightnessService: Unexpected error getting brightness: {e}")
            return 0

    def change_brightness(self, direction="up", amount=5):
        try:
            if direction == "up":
                command_list = ["brightnessctl", "s", f"+{amount}%"]
            elif direction == "down":
                command_list = ["brightnessctl", "s", f"{amount}%-"]
            else:
                return False

            subprocess.run(
                command_list,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=5,
            )
            return True

        except subprocess.CalledProcessError as e:
            logger.error(
                f"BrightnessService: Error changing brightness: {e.stderr.strip()}"
            )
            return False
        except Exception as e:
            logger.error(
                f"BrightnessService: Unexpected error changing brightness: {e}"
            )
            return False


brightness_service = BrightnessService()
