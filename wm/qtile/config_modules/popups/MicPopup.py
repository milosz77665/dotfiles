from ..services.MicService import mic_service
from .StatusPopup import StatusPopup

mic_popup = StatusPopup(
    value_getter=mic_service.get_volume,
    off_getter=mic_service.is_muted,
    filename_map=[(1, "mic.svg")],
    off_filename="mic-x.svg",
    value_formatter=lambda v: f"{v}%",
)
