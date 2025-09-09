import subprocess
from libqtile.log_utils import logger


def get_touchpad_ids():
    touchpad_ids = []
    try:
        result = subprocess.run(
            ["xinput", "list"], capture_output=True, text=True, check=True
        )
        output = result.stdout

        for line in output.splitlines():
            if "touchpad" in line.lower():
                parts = line.split()
                for i, part in enumerate(parts):
                    if "id=" in part:
                        touchpad_ids.append(part.split("=")[1])
        return touchpad_ids
    except FileNotFoundError:
        logger.error("xinput is not installed. Please install it.")
        return []
    except subprocess.CalledProcessError as e:
        logger.error(f"Error calling xinput: {e}")
        return []


def configure_touchpad():
    touchpad_ids = get_touchpad_ids()

    if touchpad_ids:
        for touchpad_id in touchpad_ids:
            tap_command = [
                "xinput",
                "set-prop",
                touchpad_id,
                "libinput Tapping Enabled",
                "1",
            ]
            try:
                subprocess.run(tap_command, check=True)
            except subprocess.CalledProcessError:
                logger.error("Failed to enable tapping.")

            button_map_command = [
                "xinput",
                "set-button-map",
                touchpad_id,
                "1",
                "0",
                "3",
                "4",
                "5",
                "6",
                "7",
            ]
            try:
                subprocess.run(button_map_command, check=True)
            except subprocess.CalledProcessError:
                logger.error("Failed to set button map.")

            natural_scroll_command = [
                "xinput",
                "set-prop",
                touchpad_id,
                "libinput Natural Scrolling Enabled",
                "1",
            ]
            try:
                subprocess.run(natural_scroll_command, check=True)
            except subprocess.CalledProcessError:
                logger.error("Failed to enable natural scrolling.")
    else:
        logger.error("No touchpad devices found.")
