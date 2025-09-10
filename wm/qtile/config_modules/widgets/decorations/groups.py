from qtile_extras.widget.groupbox2 import GroupBoxRule

from ...variables import (
    GROUPS_ACTIVE_COLOR,
    GROUPS_OCCUPIED_COLOR,
    GROUPS_EMPTY_COLOR,
    GROUPS_OTHER_SCREEN_COLOR,
)


def circles(rule, box):
    rule.text = "●"
    if box.focused:
        rule.text = "◉"
    elif box.occupied:
        rule.text = "●"
    else:
        rule.text = "○"
    return True


circles_rules = [
    GroupBoxRule().when(func=circles),
    GroupBoxRule(text_colour=GROUPS_ACTIVE_COLOR).when(
        focused=True, screen=GroupBoxRule.SCREEN_THIS
    ),
    GroupBoxRule(text_colour=GROUPS_OCCUPIED_COLOR).when(occupied=True, focused=False),
    GroupBoxRule(text_colour=GROUPS_EMPTY_COLOR).when(occupied=False),
    GroupBoxRule(text_colour=GROUPS_OTHER_SCREEN_COLOR).when(
        screen=GroupBoxRule.SCREEN_OTHER
    ),
]

numbers_rules = [
    GroupBoxRule(text_colour=GROUPS_ACTIVE_COLOR).when(
        focused=True, screen=GroupBoxRule.SCREEN_THIS
    ),
    GroupBoxRule(text_colour=GROUPS_OCCUPIED_COLOR).when(occupied=True, focused=False),
    GroupBoxRule(text_colour=GROUPS_EMPTY_COLOR).when(occupied=False),
    GroupBoxRule(text_colour=GROUPS_OTHER_SCREEN_COLOR).when(
        screen=GroupBoxRule.SCREEN_OTHER
    ),
]
