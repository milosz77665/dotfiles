import subprocess
from libqtile.log_utils import logger


class BrightnessService:
    def __init__(self):
        try:
            subprocess.check_output("which brightnessctl", shell=True)
        except subprocess.CalledProcessError:
            logger.error(
                "BrightnessService: 'brightnessctl' command not found. Please install it."
            )

    def get_brightness(self):
        try:
            output = subprocess.check_output(
                f"brightnessctl i | grep -oP '\\((\\d+)%\\)' | grep -oP '\\d+'",
                shell=True,
                text=True,
                stderr=subprocess.PIPE,
            ).strip()

            if output.isdigit():
                return int(output)

            logger.warning(
                f"BrightnessService: Cannot parse brightness percentage. Raw output: {output}"
            )
            return 0

        except subprocess.CalledProcessError as e:
            logger.error(
                f"BrightnessService: Error getting brightness (brightnessctl): {e.stderr.strip()}"
            )
            return 0
        except Exception as e:
            logger.error(f"BrightnessService: Unexpected error getting brightness: {e}")
            return 0

    def change_brightness(self, direction="up", amount="5%"):
        try:
            if direction == "up":
                command = f"brightnessctl s +{amount}"
            elif direction == "down":
                command = f"brightnessctl s {amount}-"
            else:
                return False

            subprocess.run(
                command,
                shell=True,
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
