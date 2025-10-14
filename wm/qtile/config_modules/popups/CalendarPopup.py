import calendar
from datetime import datetime, date
from qtile_extras.popup import PopupText, PopupAbsoluteLayout

from ..variables import BAR_BACKGROUND, BAR_FOREGROUND, HIGH_DPI_MULTIPLIER

EN_MONTHS = [
    "",
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
]


class CalendarPopup:
    def __init__(self):
        self.is_visible = False
        self.current_date = datetime.now().date()
        self.displayed_month = self.current_date.month
        self.displayed_year = self.current_date.year
        self.layout = None
        self.qtile = None

        self.COLOR_FOREGROUND = BAR_FOREGROUND
        self.COLOR_OTHER_MONTH = "#555555"
        self.HIGHLIGHT_COLOR = BAR_FOREGROUND
        self.COLOR_TODAY = BAR_FOREGROUND
        self.COLOR_BACKGROUND = BAR_BACKGROUND

        calendar.setfirstweekday(calendar.MONDAY)

    def _increment_month_year(self):
        if self.displayed_month == 12:
            self.displayed_month = 1
            self.displayed_year += 1
        else:
            self.displayed_month += 1

    def _decrement_month_year(self):
        if self.displayed_month == 1:
            self.displayed_month = 12
            self.displayed_year -= 1
        else:
            self.displayed_month -= 1

    def _get_month_days(self, year, month):
        cal = calendar.Calendar(firstweekday=0)
        weeks = cal.monthdatescalendar(year, month)
        return weeks

    def _day_text(self, day: date):
        text = str(day.day)
        color = self.COLOR_FOREGROUND

        if day.month != self.displayed_month:
            color = self.COLOR_OTHER_MONTH
        if day == self.current_date:
            text = f"[{day.day}]"
            color = self.COLOR_TODAY
        return text, color

    def prev_month(self):
        self._decrement_month_year()
        self._refresh_layout()

    def next_month(self):
        self._increment_month_year()
        self._refresh_layout()

    def _create_layout(self, qtile, focused_index=1):
        self.qtile = qtile
        controls = []

        weeks = self._get_month_days(self.displayed_year, self.displayed_month)
        rows_count = len(weeks)

        padding_x = int(10 * HIGH_DPI_MULTIPLIER)
        padding_y = int(15 * HIGH_DPI_MULTIPLIER)
        margin = int(15 * HIGH_DPI_MULTIPLIER)
        bigger_margin = int(25 * HIGH_DPI_MULTIPLIER)

        header_height = int(20 * HIGH_DPI_MULTIPLIER)
        weekdays_height = int(10 * HIGH_DPI_MULTIPLIER)
        week_row_height = int(10 * HIGH_DPI_MULTIPLIER)
        popup_height = (
            (rows_count - 1) * (week_row_height + margin)
            + 2 * padding_y
            + 2 * bigger_margin
            + header_height
            + weekdays_height
            + week_row_height
        )

        popup_width = int(220 * HIGH_DPI_MULTIPLIER)
        button_width = int(35 * HIGH_DPI_MULTIPLIER)
        month_year_title_width = popup_width - 2 * button_width

        month_name = EN_MONTHS[self.displayed_month]
        controls.append(
            PopupText(
                name="month_year_title",
                text=f"{month_name} {self.displayed_year}",
                pos_x=button_width,
                pos_y=padding_y,
                width=month_year_title_width,
                height=header_height,
                fontsize=int(14 * HIGH_DPI_MULTIPLIER),
                h_align="center",
                foreground=self.COLOR_FOREGROUND,
            )
        )

        controls.append(
            PopupText(
                name="prev_month_btn",
                text="",
                pos_x=padding_x,
                pos_y=padding_y,
                width=button_width,
                height=header_height,
                fontsize=int(14 * HIGH_DPI_MULTIPLIER),
                h_align="center",
                foreground=self.COLOR_FOREGROUND,
                mouse_callbacks={"Button1": self.prev_month},
                key_callbacks={"Return": self.prev_month, "Left": self.prev_month},
                can_focus=True,
                highlight=self.HIGHLIGHT_COLOR,
                highlight_method="border",
                highlight_border=0.5,
            )
        )
        controls.append(
            PopupText(
                name="next_month_btn",
                text="",
                pos_x=popup_width - padding_x - button_width,
                pos_y=padding_y,
                width=button_width,
                height=header_height,
                fontsize=int(14 * HIGH_DPI_MULTIPLIER),
                h_align="center",
                foreground=self.COLOR_FOREGROUND,
                mouse_callbacks={"Button1": self.next_month},
                key_callbacks={"Return": self.next_month, "Right": self.next_month},
                can_focus=True,
                highlight=self.HIGHLIGHT_COLOR,
                highlight_method="border",
                highlight_border=0.5,
            )
        )

        weekdays = ["M", "T", "W", "T", "F", "S", "S"]
        for i, wd in enumerate(weekdays):
            controls.append(
                PopupText(
                    name=f"wd_{i}",
                    text=wd,
                    fontsize=int(14 * HIGH_DPI_MULTIPLIER),
                    pos_x=padding_x + i * ((popup_width - 2 * padding_x) / 7.0),
                    pos_y=padding_y + bigger_margin + header_height,
                    width=(popup_width - 2 * padding_x) / 7,
                    height=weekdays_height,
                    h_align="center",
                    foreground=self.COLOR_FOREGROUND,
                )
            )

        for r, week in enumerate(weeks):
            for c, day in enumerate(week):
                text, color = self._day_text(day)
                name = f"day_{r}_{c}"
                ctrl = PopupText(
                    name=name,
                    text=text,
                    fontsize=int(14 * HIGH_DPI_MULTIPLIER),
                    pos_x=padding_x + c * ((popup_width - 2 * padding_x) / 7.0),
                    pos_y=padding_y
                    + 2 * bigger_margin
                    + header_height
                    + weekdays_height
                    + r * (week_row_height + margin),
                    width=(popup_width - 2 * padding_x) / 7.0,
                    height=week_row_height,
                    h_align="center",
                    foreground=color,
                )
                controls.append(ctrl)

        self.layout = PopupAbsoluteLayout(
            qtile,
            width=popup_width,
            height=popup_height,
            # border=self.COLOR_FOREGROUND,
            # border_width=1,
            controls=controls,
            initial_focus=focused_index,
            background=self.COLOR_BACKGROUND,
            close_on_click=True,
        )

    def _refresh_layout(self):
        focused_index = 1
        if self.layout and self.layout._focused is not None:
            focused_index = self.layout.focusable_controls.index(self.layout._focused)
        self.hide()
        self._show(self.qtile, focused_index)

    def _show(self, qtile, focused_index=1):
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
            self.displayed_month = self.current_date.month
            self.displayed_year = self.current_date.year
            self._show(qtile)
        else:
            self.hide()


calendar_popup = CalendarPopup()
