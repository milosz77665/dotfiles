import re
import subprocess
from libqtile.log_utils import logger

from ..variables import MASTER_CHANNEL


class VolumeService:
    def __init__(self, channel=MASTER_CHANNEL):
        self.channel = channel

    def get_volume(self):
        try:
            output = subprocess.check_output(
                ["amixer", "get", self.channel],
                text=True,
                stderr=subprocess.PIPE,
            ).strip()

            m = re.search(r"(\d+)%", output)
            volume = int(m.group(1)) if m else None
            return volume
        except Exception as e:
            logger.error(f"VolumeService: Error getting volume: {e}")
            return 0

    def is_muted(self):
        try:
            output = subprocess.check_output(
                ["amixer", "get", self.channel],
                text=True,
                stderr=subprocess.PIPE,
            ).strip()
            lines = output.splitlines()
            last_line = lines[-1] if lines else ""
            muted = bool(re.search(r"\[off\]", last_line))
            return muted
        except Exception as e:
            logger.error(f"VolumeService: Error checking mute status: {e}")
            return False

    def toggle_mute(self):
        try:
            subprocess.run(["amixer", "set", self.channel, "toggle"], check=True)
            return True
        except Exception as e:
            logger.error(f"VolumeService: Error toggling mute: {e}")
            return False

    def change_volume(self, direction="up", amount=2):
        arg = f"{amount}%"
        if direction == "up":
            arg += "+"
        elif direction == "down":
            arg += "-"
        try:
            subprocess.run(["amixer", "set", self.channel, arg], check=True)
            return True
        except Exception as e:
            logger.error(f"VolumeService: Error changing volume: {e}")
            return False


volume_service = VolumeService()
