from ..services.VolumeService import volume_service
from .StatusPopup import StatusPopup

volume_popup = StatusPopup(
    value_getter=volume_service.get_volume,
    off_getter=volume_service.is_muted,
    filename_map=[(60, "volume-2.svg"), (30, "volume-1.svg"), (0, "volume.svg")],
    off_filename="volume-x.svg",
    value_formatter=lambda v: f"{v}%",
)
