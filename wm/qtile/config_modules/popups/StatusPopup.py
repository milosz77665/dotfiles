from qtile_extras.popup import PopupAbsoluteLayout, PopupText, PopupImage

from ..variables import BAR_FOREGROUND, BAR_BACKGROUND, ASSETS_PATH, HIGH_DPI_MULTIPLIER


class StatusPopup:
    def __init__(
        self,
        value_getter,
        off_getter=None,
        filename_map=None,
        off_filename=None,
        value_formatter=lambda v: f"{v}%",
        popup_color=BAR_BACKGROUND,
        text_color=BAR_FOREGROUND,
        mask_color=BAR_FOREGROUND,
        assets_path=ASSETS_PATH,
    ):
        self.value_getter = value_getter
        self.off_getter = off_getter or (lambda: False)
        self.filename_map = filename_map or []
        self.off_filename = off_filename
        self.value_formatter = value_formatter
        self.POPUP_COLOR = popup_color
        self.TEXT_COLOR = text_color
        self.MASK_COLOR = mask_color
        self.ASSETS_PATH = assets_path
        self.layout = None

    def _create_layout(self, qtile):
        value = self.value_getter()
        is_off = self.off_getter()

        text = self.value_formatter(value)
        filename = next(f for level, f in self.filename_map if value >= level)

        if is_off and self.off_filename:
            filename = self.off_filename
            text = "Muted"

        margin = int(10 * HIGH_DPI_MULTIPLIER)
        icon_width = int(100 * HIGH_DPI_MULTIPLIER)
        icon_height = int(100 * HIGH_DPI_MULTIPLIER)
        text_height = int(30 * HIGH_DPI_MULTIPLIER)
        padding_y = int(20 * HIGH_DPI_MULTIPLIER)
        padding_x = int(50 * HIGH_DPI_MULTIPLIER)
        popup_width = icon_width + 2 * padding_x
        popup_height = icon_height + text_height + 2 * padding_y + margin

        controls = [
            PopupImage(
                filename=self.ASSETS_PATH + filename,
                pos_x=padding_x,
                pos_y=padding_y,
                width=icon_width,
                height=icon_height,
                mask=True,
                colour=self.MASK_COLOR,
                h_align="center",
                v_align="center",
            ),
            PopupText(
                text=text,
                pos_x=padding_x,
                pos_y=padding_y + icon_height + margin,
                width=popup_width - 2 * padding_x,
                height=text_height,
                foreground=self.TEXT_COLOR,
                fontsize=int(20 * HIGH_DPI_MULTIPLIER),
                h_align="center",
            ),
        ]

        self.layout = PopupAbsoluteLayout(
            qtile,
            width=popup_width,
            height=popup_height,
            controls=controls,
            background=self.POPUP_COLOR,
            opacity=1,
            hide_on_timeout=1,
            close_on_click=False,
        )

    def show(self, qtile):
        self._create_layout(qtile)
        screen = qtile.screens[0]
        x = (screen.width - self.layout.width) // 2
        y = screen.height - self.layout.height - 60
        self.layout.show(x=x, y=y)
