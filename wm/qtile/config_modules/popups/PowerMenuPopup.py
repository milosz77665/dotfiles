from libqtile.lazy import lazy
from qtile_extras.popup import (
    PopupAbsoluteLayout,
    PopupImage,
    PopupText,
)

from ..variables import BAR_FOREGROUND, BAR_BACKGROUND, ASSETS_PATH, HIGH_DPI_MULTIPLIER


class PowerMenuPopup:
    def __init__(
        self,
        highlight_color=BAR_FOREGROUND,
        mask_color=BAR_FOREGROUND,
        text_color=BAR_FOREGROUND,
        popup_color=BAR_BACKGROUND,
        assets_path=ASSETS_PATH,
    ):
        self.layout = None
        self.is_visible = False
        self.HIGHLIGHT_COLOR = highlight_color
        self.MASK_COLOR = mask_color
        self.TEXT_COLOR = text_color
        self.POPUP_COLOR = popup_color
        self.ASSETS_PATH = assets_path

    def _create_layout(self, qtile):
        self.qtile = qtile
        popup_elements = [
            {
                "filename": "shutdown.svg",
                "mouse_callbacks": {"Button1": lazy.spawn("shutdown now")},
                "title": "Power Off",
            },
            {
                "filename": "restart.svg",
                "mouse_callbacks": {"Button1": lazy.spawn("reboot")},
                "title": "Restart",
            },
            {
                "filename": "logout.svg",
                "mouse_callbacks": {"Button1": lazy.shutdown()},
                "title": "Log Out",
            },
        ]
        controls = []

        number_of_elements = len(popup_elements)
        number_of_margins_x = number_of_elements - 1
        padding_x = int(30 * HIGH_DPI_MULTIPLIER)
        padding_y = int(30 * HIGH_DPI_MULTIPLIER)
        margin_x = int(70 * HIGH_DPI_MULTIPLIER)
        margin_y = int(40 * HIGH_DPI_MULTIPLIER)
        image_width = int(100 * HIGH_DPI_MULTIPLIER)
        image_height = int(100 * HIGH_DPI_MULTIPLIER)
        text_height = int(30 * HIGH_DPI_MULTIPLIER)
        popup_width = (
            number_of_elements * image_width
            + 2 * padding_x
            + number_of_margins_x * margin_x
        )
        popup_height = image_height + text_height + 2 * padding_y + margin_y

        for i, element in enumerate(popup_elements):
            controls.append(
                PopupImage(
                    filename=self.ASSETS_PATH + element["filename"],
                    pos_x=padding_x
                    + i * margin_x
                    + i
                    * (
                        (popup_width - 2 * padding_x - number_of_margins_x * margin_x)
                        / number_of_elements
                    ),
                    pos_y=padding_y,
                    width=(popup_width - 2 * padding_x - number_of_margins_x * margin_x)
                    / number_of_elements,
                    height=popup_height - 2 * padding_y - margin_y - text_height,
                    mask=True,
                    highlight=self.HIGHLIGHT_COLOR,
                    highlight_method="border",
                    highlight_border=0.5,
                    colour=self.MASK_COLOR,
                    mouse_callbacks=element["mouse_callbacks"],
                ),
            )
            controls.append(
                PopupText(
                    text=element["title"],
                    pos_x=padding_x
                    + i * margin_x
                    + i
                    * (
                        (popup_width - 2 * padding_x - number_of_margins_x * margin_x)
                        / number_of_elements
                    ),
                    pos_y=padding_y + margin_y + image_height,
                    width=(popup_width - 2 * padding_x - number_of_margins_x * margin_x)
                    / number_of_elements,
                    height=text_height,
                    foreground=self.TEXT_COLOR,
                    fontsize=int(16 * HIGH_DPI_MULTIPLIER),
                    h_align="center",
                ),
            )

        self.layout = PopupAbsoluteLayout(
            qtile,
            width=popup_width,
            height=popup_height,
            controls=controls,
            # border=BAR_FOREGROUND,
            # border_width=1,
            background=self.POPUP_COLOR,
            opacity=0.9,
            initial_focus=0,
            close_on_click=True,
        )

    def _show(self, qtile):
        self._create_layout(qtile)
        self.layout.show(centered=True)
        self.is_visible = True

    def hide(self):
        if self.layout:
            try:
                self.layout.hide()
                self.is_visible = False
            except Exception:
                pass

    def toggle(self, qtile):
        if not self.is_visible:
            self._show(qtile)
        else:
            self.hide()


power_menu_popup = PowerMenuPopup()
