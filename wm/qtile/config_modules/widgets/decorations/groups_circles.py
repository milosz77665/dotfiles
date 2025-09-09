from qtile_extras.widget.groupbox2 import GroupBoxRule

from ...variables import colors


def circles(rule, box):
    if box.focused:
        rule.text = "◉"
    elif box.occupied:
        rule.text = "●"
    else:
        rule.text = "○"
    return True


rules = [
    GroupBoxRule().when(func=circles),
    GroupBoxRule(text_colour=colors["color15"]).when(
        focused=True, screen=GroupBoxRule.SCREEN_THIS
    ),
    GroupBoxRule(text_colour=colors["color2"]).when(occupied=True, focused=False),
    GroupBoxRule(text_colour=colors["color2"]).when(occupied=False),
    GroupBoxRule(text_colour=colors["color14"]).when(screen=GroupBoxRule.SCREEN_OTHER),
]
