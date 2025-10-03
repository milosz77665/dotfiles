from libqtile.widget import base
from libqtile.lazy import lazy
from libqtile.log_utils import logger
from qtile_extras.widget.mixins import TooltipMixin

from ..variables import AUDIO_APP, TOOLTIP_DEFAULTS
from ..services.VolumeService import volume_service


class VolumeWidget(base.ThreadPoolText, TooltipMixin):
    def __init__(self, **config):
        super().__init__("", **config)
        TooltipMixin.__init__(self, **config)
        self.add_defaults(TooltipMixin.defaults)
        self.add_defaults(TOOLTIP_DEFAULTS)
        self.update_interval = 0.2
        self.mouse_callbacks = {"Button1": lazy.spawn(AUDIO_APP)}
        self.icon_map = [
            (60, " "),
            (30, " "),
            (0, " "),
        ]

    def poll(self):
        is_muted = volume_service.is_muted()
        volume = volume_service.get_volume()

        if is_muted:
            self.tooltip_text = f"Muted"
            return " "
        else:
            icon = next(icon for level, icon in self.icon_map if volume >= level)
            self.tooltip_text = f"Volume: {volume}%"
            return f"{icon}"
