import subprocess
from libqtile.log_utils import logger

from ..variables import MIC_CHANNEL


class MicService:
    def __init__(self, channel=MIC_CHANNEL):
        self.channel = channel

    def get_volume(self):
        try:
            output = subprocess.check_output(
                f"amixer get {self.channel} | grep -o '[0-9]\\+%' | head -1",
                shell=True,
                text=True,
            ).strip()
            return int(output.strip("%"))
        except Exception as e:
            logger.error(f"VolumeService: Error getting mic volume: {e}")
            return 0

    def is_muted(self):
        try:
            output = subprocess.check_output(
                f"amixer get {self.channel} | grep -oP '\\[(on|off)\\]$' | head -1",
                shell=True,
                text=True,
            ).strip()
            return output == "[off]"
        except Exception as e:
            logger.error(f"VolumeService: Error checking mic mute status: {e}")
            return False

    def toggle_mute(self):
        try:
            subprocess.run(f"amixer set {self.channel} toggle", shell=True, check=True)
            return True
        except Exception as e:
            logger.error(f"VolumeService: Error toggling mic mute: {e}")
            return False

    def change_volume(self, direction="up", amount="5%"):
        command = f"amixer set {self.channel} {amount}"
        if direction == "up":
            command += "+"
        elif direction == "down":
            command += "-"

        try:
            subprocess.run(command, shell=True, check=True)
            return True
        except Exception as e:
            logger.error(f"VolumeService: Error changing mic volume: {e}")
            return False


mic_service = MicService()
