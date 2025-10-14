from qtile_extras.popup import PopupText, PopupAbsoluteLayout
from ..variables import BAR_BACKGROUND, BAR_FOREGROUND, HIGH_DPI_MULTIPLIER
from ..services.NotificationService import notification_service


class NotificationPopup:
    def __init__(self):
        self.is_visible = False
        self.layout = None
        self.qtile = None

        self.COLOR_FOREGROUND = BAR_FOREGROUND
        self.HIGHLIGHT_COLOR = BAR_FOREGROUND
        self.COLOR_BACKGROUND = BAR_BACKGROUND
        self.COLOR_DIM = "#888888"

    def _refresh_layout(self):
        focused_index = 0
        if self.layout and self.layout._focused is not None:
            focused_index = self.layout.focusable_controls.index(self.layout._focused)
        self.hide()
        self._show(self.qtile, focused_index)

    def _action_clear_all(self):
        notification_service.clear_all_notifications()
        self._refresh_layout()

    def _action_remove_one(self, notification):
        notification_service.remove_notification_by_id(notification["id"])
        self._refresh_layout()

    def _action_execute(self, notification):
        notification_service.execute_notification_action(notification["id"])
        self.hide()

    def _create_layout(self, qtile, focused_index=0):
        self.qtile = qtile
        controls = []
        notifications = notification_service.get_notifications()

        padding = int(15 * HIGH_DPI_MULTIPLIER)
        popup_width = int(350 * HIGH_DPI_MULTIPLIER)
        header_height = int(20 * HIGH_DPI_MULTIPLIER)
        item_height = int(50 * HIGH_DPI_MULTIPLIER)
        button_width = int(25 * HIGH_DPI_MULTIPLIER)
        text_to_button_gap = int(10 * HIGH_DPI_MULTIPLIER)

        controls.append(
            PopupText(
                text="󰂚  Notifications",
                pos_x=padding,
                pos_y=padding,
                width=popup_width - (padding * 3) - button_width,
                height=header_height,
                h_align="left",
                fontsize=int(14 * HIGH_DPI_MULTIPLIER),
                foreground=self.COLOR_FOREGROUND,
            )
        )

        controls.append(
            PopupText(
                text="",
                pos_x=popup_width - padding - button_width,
                pos_y=padding,
                width=button_width,
                height=header_height,
                fontsize=int(14 * HIGH_DPI_MULTIPLIER),
                foreground=self.COLOR_FOREGROUND,
                can_focus=True,
                highlight_method="border",
                highlight_border=0.5,
                highlight=self.HIGHLIGHT_COLOR,
                mouse_callbacks={"Button1": self._action_clear_all},
                key_callbacks={"Return": self._action_clear_all},
                h_align="center",
            )
        )

        current_y = padding + header_height + 10

        if not notifications:
            controls.append(
                PopupText(
                    text="No new notifications",
                    fontsize=int(14 * HIGH_DPI_MULTIPLIER),
                    pos_x=padding,
                    pos_y=current_y,
                    width=popup_width - 2 * padding,
                    height=item_height,
                    h_align="center",
                    foreground=self.COLOR_DIM,
                )
            )
            popup_height = current_y + item_height + padding
        else:
            text_width = popup_width - (2 * padding) - button_width - text_to_button_gap

            for i, notif in enumerate(notifications):
                y = current_y + (i * item_height)

                summary_text = f"{notif.get('summary', 'No Summary')}"
                controls.append(
                    PopupText(
                        text=summary_text,
                        pos_x=padding,
                        pos_y=y + 5,
                        width=text_width,
                        height=20,
                        fontsize=int(14 * HIGH_DPI_MULTIPLIER),
                        can_focus=True,
                        highlight=self.HIGHLIGHT_COLOR,
                        highlight_method="border",
                        highlight_border=0.5,
                        foreground=self.COLOR_FOREGROUND,
                        mouse_callbacks={
                            "Button1": lambda n=notif: self._action_execute(n)
                        },
                        key_callbacks={
                            "Return": lambda n=notif: self._action_execute(n)
                        },
                        h_align="left",
                    )
                )

                body_text = notif.get("body", "")
                if len(body_text) > 40:
                    body_text = body_text[:37] + "..."
                controls.append(
                    PopupText(
                        text=body_text,
                        pos_x=padding,
                        pos_y=y + 30,
                        fontsize=int(14 * HIGH_DPI_MULTIPLIER),
                        width=text_width,
                        height=15,
                        h_align="left",
                        foreground=self.COLOR_DIM,
                    )
                )

                controls.append(
                    PopupText(
                        text="",
                        pos_x=popup_width - padding - button_width,
                        pos_y=y + (item_height / 2) - (header_height / 2),
                        width=button_width,
                        height=header_height,
                        foreground=self.COLOR_FOREGROUND,
                        fontsize=int(14 * HIGH_DPI_MULTIPLIER),
                        can_focus=True,
                        highlight=self.HIGHLIGHT_COLOR,
                        highlight_method="border",
                        highlight_border=0.5,
                        mouse_callbacks={
                            "Button1": lambda n=notif: self._action_remove_one(n)
                        },
                        key_callbacks={
                            "Return": lambda n=notif: self._action_remove_one(n)
                        },
                        h_align="center",
                    )
                )

            popup_height = current_y + (len(notifications) * item_height) + padding

        self.layout = PopupAbsoluteLayout(
            qtile,
            width=popup_width,
            height=popup_height,
            controls=controls,
            initial_focus=focused_index,
            background=self.COLOR_BACKGROUND,
            close_on_click=True,
        )

    def _show(self, qtile, focused_index=0):
        self._create_layout(qtile, focused_index)
        self.layout.show(relative_to=3, relative_to_bar=True)
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


notification_popup = NotificationPopup()
