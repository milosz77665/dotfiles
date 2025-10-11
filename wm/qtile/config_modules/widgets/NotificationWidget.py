from libqtile.widget import base
from qtile_extras.widget.mixins import TooltipMixin

from ..variables import FAST_UPDATE_INTERVAL, TOOLTIP_DEFAULTS
from ..services.NotificationService import notification_service


class NotificationWidget(base.ThreadPoolText, TooltipMixin):
    def __init__(self, **config):
        super().__init__("", **config)
        TooltipMixin.__init__(self, **config)
        self.add_defaults(TooltipMixin.defaults)
        self.add_defaults(TOOLTIP_DEFAULTS)
        self.update_interval = FAST_UPDATE_INTERVAL
        self.icon = ""

    def poll(self):
        count = notification_service.get_count()
        self.tooltip_text = f"Notifications: {count}"

        if count > 0:
            return f"{self.icon} " + f"<span rise='6000' size='small'>{count}</span>"
        else:
            return f"{self.icon} "
