import re
import subprocess
from libqtile.log_utils import logger

from ..variables import MIC_CHANNEL


class MicService:
    def __init__(self, channel=MIC_CHANNEL):
        self.channel = channel

    def get_volume(self):
        try:
            output = subprocess.check_output(
                ["amixer", "get", self.channel],
                text=True,
                stderr=subprocess.PIPE,
            ).strip()
            m = re.search(r"(\d+)%", output)
            vol = int(m.group(1)) if m else None
            return vol
        except Exception as e:
            logger.error(f"VolumeService: Error getting mic volume: {e}")
            return 0

    def is_muted(self):
        try:
            output = subprocess.check_output(
                ["amixer", "get", self.channel],
                text=True,
                stderr=subprocess.PIPE,
            ).strip()
            m2 = re.search(r"\[(on|off)\]", output.splitlines()[-1] if output else "")
            muted = (m2.group(1) == "off") if m2 else None
            return muted
        except Exception as e:
            logger.error(f"VolumeService: Error checking mic mute status: {e}")
            return False

    def toggle_mute(self):
        try:
            subprocess.run(["amixer", "set", self.channel, "toggle"], check=True)
            return True
        except Exception as e:
            logger.error(f"VolumeService: Error toggling mic mute: {e}")
            return False

    def change_volume(self, direction="up", amount=5):
        arg = f"{amount}%"
        if direction == "up":
            arg += "+"
        elif direction == "down":
            arg += "-"
        try:
            subprocess.run(["amixer", "set", self.channel, arg], check=True)
            return True
        except Exception as e:
            logger.error(f"VolumeService: Error changing mic volume: {e}")
            return False


mic_service = MicService()
