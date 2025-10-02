from qtile_extras.widget.groupbox2 import GroupBoxRule

from ..variables import (
    GROUPS_ACTIVE_COLOR,
    GROUPS_OCCUPIED_COLOR,
    GROUPS_EMPTY_COLOR,
    GROUPS_OTHER_SCREEN_COLOR,
)


def retro_numbers_label(rule, box):
    label = ""
    group = box.group
    name = group.name
    count = len(group.windows)

    screen = group.screen.index if group.screen else None

    if screen == 0:
        screen = "A"
    elif screen == 1:
        screen = "B"
    elif screen == 2:
        screen = "C"
    elif screen == 3:
        screen = "D"

    label += f"[{name}]" if box.focused else name

    if count > 0:
        label += f"<span rise='6000' size='small'>{count}</span>"

    if screen is not None:
        label += f"<span rise='-6000' size='small'>{screen}</span>"

    rule.text = label
    return True


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

retro_numbers_rules = [
    GroupBoxRule().when(func=retro_numbers_label),
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
