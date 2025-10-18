from libqtile.lazy import lazy
from libqtile.config import Key, Drag, Click
from libqtile import qtile
from libqtile.utils import guess_terminal

from .utils.feh import change_wallpaper
from .variables import MOD, TERMINAL, BROWSER, CODE_EDITOR, TEXT_EDITOR, NOTES, GROUPS
from .popups.CalendarPopup import calendar_popup
from .popups.PowerMenuPopup import power_menu_popup
from .popups.MenuPopup import menu_popup
from .popups.VolumePopup import volume_popup
from .popups.MicPopup import mic_popup
from .popups.BrightnessPopup import brightness_popup
from .popups.NotificationPopup import notification_popup
from .services.BrightnessService import brightness_service
from .services.VolumeService import volume_service
from .services.MicService import mic_service
from .services.AirplaneModeService import airplane_mode_service


if not TERMINAL:
    TERMINAL = guess_terminal()


def close_all_popups(qtile):
    if calendar_popup.is_visible:
        calendar_popup.hide()
    if power_menu_popup.is_visible:
        power_menu_popup.hide()
    if notification_popup.is_visible:
        notification_popup.hide()
    if menu_popup.is_visible:
        menu_popup.hide()


def run_service_function(function, *args):
    if menu_popup.is_visible:
        menu_popup.hide()
    function(*args)


def change_value_and_show_status(qtile, target, direction, amount):
    if target == "volume":
        volume_service.change_volume(direction, amount)
        volume_popup.show(qtile)
    elif target == "brightness":
        brightness_service.change_brightness(direction, amount)
        brightness_popup.show(qtile)
    elif target == "mic":
        mic_service.change_volume(direction, amount)
        mic_popup.show(qtile)
    menu_popup.hide()


def toggle_mute_and_show_status(qtile, target):
    if target == "volume":
        volume_service.toggle_mute()
        volume_popup.show(qtile)
    elif target == "mic":
        mic_service.toggle_mute()
        mic_popup.show(qtile)
    menu_popup.hide()


keys = [
    # A list of available commands that can be bound to keys can be found
    # at https://docs.qtile.org/en/latest/manual/config/lazy.html
    #############################
    ######## Launch Apps ########
    #############################
    Key(["control", "mod1"], "t", lazy.spawn(TERMINAL), desc="Launch terminal"),
    Key([MOD], "r", lazy.spawn("rofi -show drun"), desc="Launch Rofi"),
    Key([MOD], "b", lazy.spawn(BROWSER), desc="Launch Browser"),
    Key([MOD], "z", lazy.spawn(CODE_EDITOR), desc="Launch Code Editor"),
    Key([MOD], "a", lazy.spawn(TEXT_EDITOR), desc="Launch Text Editor"),
    Key([MOD], "s", lazy.spawn(NOTES), desc="Launch Notes"),
    Key([MOD], "p", lazy.spawn("arandr"), desc="Launch Arandr"),
    Key(
        ["control", "mod1"],
        "c",
        lazy.function(lambda qtile: calendar_popup.toggle(qtile)),
        desc="Toggle calendar",
    ),
    Key(
        [MOD],
        "u",
        lazy.function(lambda qtile: menu_popup.toggle(qtile)),
        desc="Toggle menu popup",
    ),
    Key(
        ["control", "mod1"],
        "n",
        lazy.function(lambda qtile: notification_popup.toggle(qtile)),
        desc="Toggle notification popup",
    ),
    Key(
        ["control", "mod1"],
        "h",
        lazy.widget["widgetbox"].toggle(),
        desc="Toggle mpris2",
    ),
    Key(
        [MOD],
        "Escape",
        lazy.function(close_all_popups),
        desc="Close all popups",
    ),
    #############################
    ####### Function Keys #######
    #############################
    Key(
        [],
        "XF86MonBrightnessUp",
        lazy.function(
            lambda qtile: run_service_function(
                change_value_and_show_status, qtile, "brightness", "up", 5
            )
        ),
        desc="Increase brightness",
    ),
    Key(
        [],
        "XF86MonBrightnessDown",
        lazy.function(
            lambda qtile: run_service_function(
                change_value_and_show_status, qtile, "brightness", "down", 5
            )
        ),
        desc="Decrease brightness",
    ),
    Key(
        [],
        "XF86AudioRaiseVolume",
        lazy.function(
            lambda qtile: run_service_function(
                change_value_and_show_status, qtile, "volume", "up", 2
            )
        ),
        desc="Increase volume",
    ),
    Key(
        [],
        "XF86AudioLowerVolume",
        lazy.function(
            lambda qtile: run_service_function(
                change_value_and_show_status, qtile, "volume", "down", 2
            )
        ),
        desc="Decrease volume",
    ),
    Key(
        [],
        "XF86AudioMute",
        lazy.function(
            lambda qtile: run_service_function(
                toggle_mute_and_show_status, qtile, "volume"
            )
        ),
        desc="Toggle mute",
    ),
    Key(
        ["mod1"],
        "XF86AudioRaiseVolume",
        lazy.function(
            lambda qtile: run_service_function(
                change_value_and_show_status, qtile, "mic", "up", 2
            )
        ),
        desc="Increase mic volume",
    ),
    Key(
        ["mod1"],
        "XF86AudioLowerVolume",
        lazy.function(
            lambda qtile: run_service_function(
                change_value_and_show_status, qtile, "mic", "down", 2
            )
        ),
        desc="Decrease mic volume",
    ),
    Key(
        [],
        "XF86AudioMicMute",
        lazy.function(
            lambda qtile: run_service_function(
                toggle_mute_and_show_status, qtile, "mic"
            )
        ),
        desc="Toggle mic mute",
    ),
    Key(
        ["mod1"],
        "XF86AudioMute",
        lazy.function(
            lambda qtile: run_service_function(
                toggle_mute_and_show_status, qtile, "mic"
            )
        ),
        desc="Toggle mic mute",
    ),
    Key(
        [],
        "Print",
        lazy.spawn(f"flameshot gui"),
        desc="Start manual capture in GUI mode",
    ),
    Key(
        ["mod1"],
        "Print",
        lazy.spawn(f"flameshot screen"),
        desc="Capture a single screen",
    ),
    Key(
        ["control"],
        "Print",
        lazy.spawn(f"flameshot full"),
        desc="Capture the entire desktop",
    ),
    Key(
        [MOD, "control"],
        "n",
        lazy.widget["music_player"].next(),
        desc="Play the next track",
    ),
    Key(
        [MOD, "control"],
        "b",
        lazy.widget["music_player"].previous(),
        desc="Play the previous track",
    ),
    Key(
        [MOD, "control"],
        "p",
        lazy.widget["music_player"].play_pause(),
        desc="Toggle the playback status",
    ),
    Key(
        ["mod1"],
        "s",
        lazy.function(
            lambda qtile: run_service_function(
                airplane_mode_service.toggle_airplane_mode, qtile
            )
        ),
        desc="Enter airplane mode",
    ),
    ############################
    ##### Change Win Focus #####
    ############################
    # Switch between windows
    Key([MOD], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([MOD], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([MOD], "j", lazy.layout.down(), desc="Move focus down"),
    Key([MOD], "k", lazy.layout.up(), desc="Move focus up"),
    Key([MOD], "space", lazy.layout.next(), desc="Move window focus to other window"),
    #############################
    ######### Move Wins #########
    #############################
    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key(
        [MOD, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"
    ),
    Key(
        [MOD, "shift"],
        "l",
        lazy.layout.shuffle_right(),
        desc="Move window to the right",
    ),
    Key([MOD, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([MOD, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    #############################
    ######### Grow Wins #########
    #############################
    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([MOD, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key(
        [MOD, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"
    ),
    Key([MOD, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([MOD, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([MOD], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    #############################
    ##### Split vs Unsplit ######
    #############################
    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key(
        [MOD, "shift"],
        "Return",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
    ),
    #############################
    ###### Change Layouts #######
    #############################
    # Toggle between different layouts as defined below
    Key([MOD], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key(
        [MOD],
        "f",
        lazy.window.toggle_fullscreen(),
        desc="Toggle fullscreen on the focused window",
    ),
    Key(
        [MOD],
        "t",
        lazy.window.toggle_floating(),
        desc="Toggle floating on the focused window",
    ),
    #############################
    ######## Close Win  #########
    #############################
    Key([MOD], "c", lazy.window.kill(), desc="Kill focused window"),
    ############################
    ##### Power Management #####
    ############################
    Key(
        [MOD, "mod1"],
        "l",
        lazy.spawn("betterlockscreen -l"),
        desc="Lock the screen",
    ),
    ##############################
    ########### Picom ############
    ##############################
    Key(
        [MOD, "control"],
        "Down",
        lazy.spawn("picom-trans --current -5"),
        desc="Increase active window transparency",
    ),
    Key(
        [MOD, "control"],
        "Up",
        lazy.spawn("picom-trans --current +5"),
        desc="Decrease active window transparency",
    ),
    Key(
        [MOD, "control"],
        "o",
        lazy.spawn("picom-trans --current --opacity 100"),
        desc="Set active window to opaque",
    ),
    Key(
        [MOD, "control"],
        "d",
        lazy.spawn("picom-trans -r"),
        desc="Reset active window transparency to default (picom.conf)",
    ),
    ##############################
    ########### Qtile ############
    ##############################
    Key([MOD, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key(
        [MOD, "control"],
        "q",
        lazy.function(lambda qtile: power_menu_popup.toggle(qtile)),
        desc="Shutdown Qtile",
    ),
    Key(
        [MOD, "control"],
        "t",
        lazy.spawncmd(),
        desc="Spawn a command using a prompt widget",
    ),
    Key(
        [MOD, "shift"],
        "w",
        change_wallpaper,
        desc="Change wallpaper",
    ),
]

#############################
########## Groups ###########
#############################
for i in GROUPS:
    keys.extend(
        [
            # mod + group number = switch to group
            Key(
                [MOD],
                i.name,
                lazy.group[i.name].toscreen(),
                desc=f"Switch to group {i.name}",
            ),
            # mod + shift + group number = switch to & move focused window to group
            Key(
                [MOD, "shift"],
                i.name,
                lazy.window.togroup(i.name, switch_group=True),
                desc=f"Switch to & move focused window to group {i.name}",
            ),
            # Or, use below if you prefer not to switch to that group.
            # # mod + shift + group number = move focused window to group
            # Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
            #     desc="move focused window to group {}".format(i.name)),
        ]
    )

##############################
########### Mouse ############
##############################
# Drag floating layouts.
mouse = [
    Drag(
        [MOD],
        "Button1",
        lazy.window.set_position_floating(),
        start=lazy.window.get_position(),
    ),
    Drag(
        [MOD], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()
    ),
    Click([MOD], "Button2", lazy.window.bring_to_front()),
]

# Add key bindings to switch VTs in Wayland.
# We can't check qtile.core.name in default config as it is loaded before qtile is started
# We therefore defer the check until the key binding is run by using .when(func=...)
for vt in range(1, 8):
    keys.append(
        Key(
            ["control", "mod1"],
            f"f{vt}",
            lazy.core.change_vt(vt).when(func=lambda: qtile.core.name == "wayland"),
            desc=f"Switch to VT{vt}",
        )
    )
