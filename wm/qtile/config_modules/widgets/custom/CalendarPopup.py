import calendar
from datetime import datetime, date
from qtile_extras.popup import PopupRelativeLayout, PopupText
from ...variables import BAR_BACKGROUND, BAR_FOREGROUND

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
        self.focused_arrow_index = 1
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

    def _create_layout(self, qtile):
        """(Re)build whole popup for current displayed_month/displayed_year."""
        self.qtile = qtile
        controls = []

        weeks = self._get_month_days(self.displayed_year, self.displayed_month)
        rows_count = len(weeks)

        month_name = EN_MONTHS[self.displayed_month]
        controls.append(
            PopupText(
                name="month_year_title",
                text=f"{month_name} {self.displayed_year}",
                pos_x=0,
                pos_y=0,
                width=1,
                height=0.1,
                fontsize=14,
                h_align="center",
                foreground=self.COLOR_FOREGROUND,
            )
        )

        controls.append(
            PopupText(
                name="prev_month_btn",
                text="",
                pos_x=0.0,
                pos_y=0.15,
                width=0.15,
                height=0.1,
                fontsize=14,
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
                pos_x=0.85,
                pos_y=0.15,
                width=0.15,
                height=0.1,
                fontsize=14,
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
                    pos_x=i * (1.0 / 7.0),
                    pos_y=0.3,
                    width=1.0 / 7.0,
                    height=0.1,
                    h_align="center",
                    foreground=self.COLOR_FOREGROUND,
                )
            )

        start_y = 0.4
        cell_h = 0.1
        for r, week in enumerate(weeks):
            for c, day in enumerate(week):
                text, color = self._day_text(day)
                name = f"day_{r}_{c}"
                ctrl = PopupText(
                    name=name,
                    text=text,
                    pos_x=c * (1.0 / 7.0),
                    pos_y=start_y + r * cell_h,
                    width=1.0 / 7.0,
                    height=cell_h,
                    h_align="center",
                    foreground=color,
                )
                controls.append(ctrl)

        total_height_fraction = 0.5 + rows_count * cell_h
        base_pixel = 200
        height_px = int(base_pixel * total_height_fraction)

        self.layout = PopupRelativeLayout(
            qtile,
            width=220,
            height=height_px,
            border=self.COLOR_FOREGROUND,
            border_width=1,
            controls=controls,
            background=self.COLOR_BACKGROUND,
            initial_focus=self.focused_arrow_index,
            close_on_click=True,
            key_callbacks={
                "Escape": lambda: self.toggle(qtile),
            },
        )

    def prev_month(self, *args):
        self.focused_arrow_index = 0
        if self.layout:
            try:
                self.layout.hide()
            except Exception:
                pass
        self._decrement_month_year()
        self._create_layout(self.qtile)

        self.layout.show(x=-0.002, relative_to=3, relative_to_bar=True)
        self.is_visible = True

    def next_month(self, *args):
        self.focused_arrow_index = 1
        if self.layout:
            try:
                self.layout.hide()
            except Exception:
                pass
        self._increment_month_year()
        self._create_layout(self.qtile)
        self.layout.show(x=-0.002, relative_to=3, relative_to_bar=True)
        self.is_visible = True

    def toggle(self, qtile):
        if not self.is_visible:
            self.displayed_month = self.current_date.month
            self.displayed_year = self.current_date.year

            self._create_layout(qtile)
            self.layout.show(x=-0.002, relative_to=3, relative_to_bar=True)
            self.is_visible = True
        else:
            if self.layout:
                self.layout.hide()
            self.is_visible = False


calendar_popup = CalendarPopup()


def toggle_calendar_popup(qtile):
    calendar_popup.toggle(qtile)
