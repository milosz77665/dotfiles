from ..services.BrightnessService import brightness_service
from .StatusPopup import StatusPopup

brightness_popup = StatusPopup(
    value_getter=brightness_service.get_brightness,
    filename_map=[(1, "brightness.svg")],
    value_formatter=lambda v: f"{v}%",
)
