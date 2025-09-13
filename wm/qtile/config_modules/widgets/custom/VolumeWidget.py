from libqtile.widget import base
from libqtile.lazy import lazy
from libqtile.log_utils import logger
import subprocess
from qtile_extras.widget.mixins import TooltipMixin

from ...variables import AUDIO_APP, TOOLTIP_DEFAULTS


class VolumeWidget(base.ThreadPoolText, TooltipMixin):
    def __init__(self, **config):
        super().__init__("", **config)
        TooltipMixin.__init__(self, **config)
        self.add_defaults(TooltipMixin.defaults)
        self.add_defaults(TOOLTIP_DEFAULTS)
        self.update_interval = 0.2
        self.mouse_callbacks = {
            "Button1": lazy.spawn(AUDIO_APP),
            "Button3": lazy.function(self.toggle_mute),
        }

    def _get_wifi_icon(self, volume):
        if volume == 0:
            return " "
        elif volume <= 50:
            return " "
        else:
            return " "

    def poll(self):
        try:
            muted_output = subprocess.check_output(
                "amixer get Master | grep -o '\\[off\\]' || true",
                shell=True,
                text=True,
            ).strip()

            if muted_output:
                self.tooltip_text = f"Volume: 0%"
                return ""

            output = subprocess.check_output(
                "amixer get Master | grep -o '[0-9]\\+%' | head -1",
                shell=True,
                text=True,
            ).strip()

            volume = int(output.strip("%"))
            icon = self._get_wifi_icon(volume)
            self.tooltip_text = f"Volume: {volume}%"
            return f"{icon}"
        except Exception as e:
            logger.error(f"Volume error: {e}")
            return "󰝟 ERR"

    def toggle_mute(self, qtile):
        qtile.spawn("amixer set Master toggle")
