from libqtile import layout

from .variables import (
    WINDOWS_MARGIN,
    WINDOWS_BORDER,
    WINDOW_BORDER_FOCUS_COLOR,
    WINDOW_BORDER_NORMAL_COLOR,
)


layouts = [
    layout.Columns(
        border_focus=WINDOW_BORDER_FOCUS_COLOR,
        border_focus_stack=WINDOW_BORDER_FOCUS_COLOR,
        border_normal=WINDOW_BORDER_NORMAL_COLOR,
        border_normal_stack=WINDOW_BORDER_NORMAL_COLOR,
        border_width=WINDOWS_BORDER,
        fair=True,
        margin=WINDOWS_MARGIN,
    ),
    layout.Max(),
    # Try more layouts by unleashing below layouts.
    layout.Stack(num_stacks=2),
    layout.Bsp(),
    layout.Matrix(),
    layout.MonadTall(),
    layout.MonadWide(),
    layout.RatioTile(),
    layout.Tile(),
    layout.TreeTab(),
    layout.VerticalTile(),
    layout.Zoomy(),
]
