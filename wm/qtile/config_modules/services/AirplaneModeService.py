from .WlanService import wlan_service
from .BluetoothService import bt_service


class AirplaneModeService:
    def get_status(self):
        return not wlan_service.get_status() and not bt_service.get_status()

    def _enable_airplane_mode(self, qtile):
        if wlan_service.get_status():
            wlan_service.toggle_state(qtile)
        if bt_service.get_status():
            bt_service.toggle_state(qtile)

    def _disable_airplane_mode(self, qtile):
        if not wlan_service.get_status():
            wlan_service.toggle_state(qtile)
        if not bt_service.get_status():
            bt_service.toggle_state(qtile)

    def toggle_airplane_mode(self, qtile):
        if self.get_status():
            self._disable_airplane_mode(qtile)
        else:
            self._enable_airplane_mode(qtile)


airplane_mode_service = AirplaneModeService()
