from libqtile import bar
from libqtile.config import Screen

from .variables import (
    BAR_HEIGHT,
    BAR_MARGIN,
    BAR_BACKGROUND,
)

# from .widgets.widgets_modern import get_widget_list
from .widgets_retro import get_widget_list


screens = [
    Screen(
        top=bar.Bar(
            get_widget_list(is_primary=True),
            BAR_HEIGHT,
            background=BAR_BACKGROUND,
            margin=BAR_MARGIN,
        ),
        # You can uncomment this variable if you see that on X11 floating resize/moving is laggy
        # By default we handle these events delayed to already improve performance, however your system might still be struggling
        # This variable is set to None (no cap) by default, but you can set it to 60 to indicate that you limit it to 60 events per second
        # x11_drag_polling_rate = 60,
    ),
    Screen(
        top=bar.Bar(
            get_widget_list(),
            BAR_HEIGHT,
            background=BAR_BACKGROUND,
            margin=BAR_MARGIN,
        ),
    ),
]
