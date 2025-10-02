from qtile_extras.widget.decorations import RectDecoration

from ..variables import (
    PILL_COLOR,
    PILL_RADIUS,
    PADDING,
    PILL_LINE_COLOR,
    PILL_LINE_WIDTH,
)


pill_deco = {
    "decorations": [
        RectDecoration(
            colour=PILL_COLOR,
            radius=PILL_RADIUS,
            filled=True,
            padding_y=0,
            padding_x=0,
            group=True,
            line_colour=PILL_LINE_COLOR,
            line_width=PILL_LINE_WIDTH,
        )
    ],
    "padding": PADDING,
}
