import re
import subprocess
from libqtile.log_utils import logger


def get_touchpad_id(touchpad_name):
    try:
        output = subprocess.check_output(["xinput", "--list"], universal_newlines=True)
        for line in output.splitlines():
            if touchpad_name in line and "pointer" in line:
                match = re.search(r"id=(\d+)", line)
                if match:
                    return match.group(1)
        return None
    except Exception as e:
        logger.error(f"Błąd podczas pobierania ID touchpada: {e}")
        return None
