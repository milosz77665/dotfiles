import subprocess
from libqtile.log_utils import logger

from variables import MASTER_CHANNEL


class VolumeService:
    def __init__(self, channel=MASTER_CHANNEL):
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
            logger.error(f"VolumeService: Error getting volume: {e}")
            return 0

    def is_muted(self):
        try:
            output = subprocess.check_output(
                f"amixer get {self.channel} | grep -o '\\[off\\]' || true",
                shell=True,
                text=True,
            ).strip()
            return bool(output)
        except Exception as e:
            logger.error(f"VolumeService: Error checking mute status: {e}")
            return False

    def toggle_mute(self):
        try:
            subprocess.run(f"amixer set {self.channel} toggle", shell=True, check=True)
            return True
        except Exception as e:
            logger.error(f"VolumeService: Error toggling mute: {e}")
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
            logger.error(f"VolumeService: Error changing volume: {e}")
            return False
