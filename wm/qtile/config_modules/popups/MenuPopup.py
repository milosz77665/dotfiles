from libqtile.lazy import lazy
from qtile_extras.popup import PopupAbsoluteLayout, PopupText, PopupImage
import threading

from ..variables import BAR_FOREGROUND, BAR_BACKGROUND, ASSSETS_PATH
from ..services.BatteryService import battery_service
from ..services.BluetoothService import bt_service
from ..services.BrightnessService import brightness_service
from ..services.MicService import mic_service
from ..services.VolumeService import volume_service
from ..services.WlanService import wlan_service
from ..services.AirplaneModeService import airplane_mode_service


class MenuPopup:
    def __init__(
        self,
        highlight_color=BAR_FOREGROUND,
        popup_color=BAR_BACKGROUND,
        text_color=BAR_FOREGROUND,
        mask_color=BAR_FOREGROUND,
        assets_path=ASSSETS_PATH,
    ):
        self.focused_index = 0
        self.layout = None
        self.qtile = None
        self.is_visible = False
        self.available_networks = []
        self.wlan_page = 0
        self.wlan_items_per_page = 6
        self.bt_items_per_page = 6
        self.available_bt_devices = []
        self.bt_page = 0
        self.is_wlan_list_expanded = False
        self.is_bt_list_expanded = False
        self.POPUP_COLOR = popup_color
        self.TEXT_COLOR = text_color
        self.MASK_COLOR = mask_color
        self.HIGHLIGHT_COLOR = highlight_color
        self.ASSETS_PATH = assets_path
        self.volume_filename_map = [
            (60, "volume-2.svg"),
            (30, "volume-1.svg"),
            (0, "volume.svg"),
        ]
        self.wlan_icon_map = [
            (90, "󰤨 "),
            (70, "󰤥 "),
            (40, "󰤢 "),
            (1, "󰤟 "),
            (0, "󰤯 "),
        ]
        self.battery_icon_map = [
            (100, "󰁹"),
            (90, "󰂂"),
            (80, "󰂁"),
            (70, "󰂀"),
            (60, "󰁿"),
            (50, "󰁾"),
            (40, "󰁽"),
            (30, "󰁼"),
            (20, "󰁻"),
            (10, "󰁺"),
            (0, "󰂎"),
        ]

    def _get_volume_data(self):
        volume = volume_service.get_volume()
        is_volume_muted = volume_service.is_muted()
        filename = next(f for level, f in self.volume_filename_map if volume >= level)
        volume_text = f"{volume}%"
        if is_volume_muted:
            filename = "volume-x.svg"
            volume_text = "Muted"
        return volume_text, filename

    def _get_mic_data(self):
        mic_volume = mic_service.get_volume()
        is_mic_muted = mic_service.is_muted()
        if is_mic_muted:
            filename = "mic-x.svg"
            mic_text = "Muted"
        else:
            filename = "mic.svg"
            mic_text = f"{mic_volume}%"
        return mic_text, filename

    def _get_brightness_data(self):
        return f"{brightness_service.get_brightness()}%"

    def _calculate_wlan_extra_height(self, section_height):
        extra_height = 0
        if self.is_wlan_list_expanded:
            list_len = min(len(self.available_networks), self.wlan_items_per_page)
            if list_len == 0:
                list_len = 1
            extra_height += list_len * (section_height + 5) + 10

        return extra_height

    def _calculate_bt_extra_height(self, section_height):
        extra_height = 0
        if self.is_bt_list_expanded:
            list_len = min(len(self.available_bt_devices), self.bt_items_per_page)
            if list_len == 0:
                list_len = 1
            extra_height += list_len * (section_height + 5) + 10

        return extra_height

    def _create_layout(self, qtile):
        self.qtile = qtile
        controls = []

        volume_text, volume_filename = self._get_volume_data()
        mic_text, mic_filename = self._get_mic_data()
        brightness_text = self._get_brightness_data()

        icon_width = 25
        list_offset = 40
        image_height = 30
        section_height = image_height
        text_width = 70
        margin_x = 10
        margin_y = 20
        list_margin_y = 5
        padding_y = 20
        padding_x = 20
        popup_width = 400
        bt_extra_height = self._calculate_bt_extra_height(section_height)
        wlan_extra_height = self._calculate_wlan_extra_height(section_height)
        bt_connected_extra = 0

        ########################################################
        ###################### WLAN SECTION ####################
        ########################################################
        is_wifi_enabled = wlan_service.get_status()

        if is_wifi_enabled:
            ssid = wlan_service.get_ssid()
            ip_address = wlan_service.get_ip_address()
            signal = wlan_service.get_signal_strength()
            wlan_icon = next(
                icon for level, icon in self.wlan_icon_map if signal >= level
            )

            controls.append(
                PopupText(
                    text="▼" if self.is_wlan_list_expanded else "▶",
                    pos_x=padding_x,
                    pos_y=padding_y,
                    width=icon_width,
                    height=section_height,
                    fontsize=12,
                    can_focus=True,
                    highlight=self.HIGHLIGHT_COLOR,
                    highlight_method="border",
                    highlight_border=0.5,
                    mouse_callbacks={"Button1": self._toggle_wifi_list},
                    h_align="center",
                    v_align="middle",
                )
            )
            controls.append(
                PopupText(
                    text=wlan_icon,
                    pos_x=padding_x + icon_width + margin_x,
                    pos_y=padding_y,
                    width=icon_width,
                    height=section_height,
                    fontsize=18,
                    can_focus=True,
                    highlight=self.HIGHLIGHT_COLOR,
                    highlight_method="border",
                    highlight_border=0.5,
                    h_align="center",
                    v_align="middle",
                    mouse_callbacks={"Button1": self._toggle_wifi_state},
                )
            )
            controls.append(
                PopupText(
                    text=ssid,
                    pos_x=padding_x + 2 * icon_width + 2 * margin_x,
                    pos_y=padding_y,
                    width=(popup_width - 2 * padding_x - 2 * margin_x - 2 * icon_width)
                    / 2,
                    height=section_height,
                    fontsize=16,
                    h_align="center",
                    v_align="middle",
                )
            )
            controls.append(
                PopupText(
                    text=ip_address,
                    pos_x=padding_x
                    + 2 * icon_width
                    + 2 * margin_x
                    + (popup_width - 2 * padding_x - 2 * margin_x - 2 * icon_width) / 2,
                    pos_y=padding_y,
                    width=(popup_width - 2 * padding_x - 2 * margin_x - 2 * icon_width)
                    / 2,
                    height=section_height,
                    fontsize=16,
                    h_align="center",
                    v_align="middle",
                )
            )

            if self.is_wlan_list_expanded:
                wlan_list_pos_y = padding_y + section_height + list_margin_y

                if not self.available_networks:
                    controls.append(
                        PopupText(
                            text="Scanning for Wi-Fi...",
                            pos_x=padding_x + list_offset,
                            pos_y=wlan_list_pos_y,
                            width=popup_width - 2 * padding_x - 40,
                            height=section_height,
                            fontsize=14,
                            h_align="left",
                            v_align="middle",
                        )
                    )
                else:
                    start = self.wlan_page * self.wlan_items_per_page
                    end = start + self.wlan_items_per_page
                    page_networks = self.available_networks[start:end]

                    for i, network in enumerate(page_networks):
                        ssid = network["ssid"]
                        signal = network["signal"]
                        security = network["security"]
                        icon = next(
                            icon
                            for level, icon in self.wlan_icon_map
                            if signal >= level
                        )
                        controls.append(
                            PopupText(
                                text=f"{icon}  {ssid} {security}",
                                pos_x=padding_x + list_offset,
                                pos_y=wlan_list_pos_y
                                + i * (section_height + list_margin_y),
                                width=popup_width - 2 * padding_x - list_offset,
                                height=section_height,
                                fontsize=14,
                                can_focus=True,
                                highlight=self.HIGHLIGHT_COLOR,
                                highlight_method="border",
                                highlight_border=0.5,
                                mouse_callbacks={
                                    "Button1": lazy.function(
                                        lambda q, s=ssid: wlan_service.connect_to_network(
                                            s
                                        )
                                    )
                                },
                            )
                        )

                    if self.wlan_page > 0:
                        controls.append(
                            PopupText(
                                text="↑",
                                pos_x=popup_width - padding_x,
                                pos_y=wlan_list_pos_y - padding_y,
                                width=20,
                                height=20,
                                fontsize=14,
                                mouse_callbacks={"Button1": self._prev_wifi_page},
                            )
                        )
                    if len(self.available_networks) > end:
                        controls.append(
                            PopupText(
                                text="↓",
                                pos_x=popup_width - padding_x,
                                pos_y=wlan_list_pos_y
                                + self.wlan_items_per_page * (section_height + 5),
                                width=20,
                                height=20,
                                fontsize=14,
                                mouse_callbacks={"Button1": self._next_wifi_page},
                            )
                        )
        else:
            controls.append(
                PopupText(
                    text="󰤭",
                    pos_x=padding_x,
                    pos_y=padding_y,
                    width=icon_width,
                    height=section_height,
                    fontsize=18,
                    can_focus=True,
                    highlight=self.HIGHLIGHT_COLOR,
                    highlight_method="border",
                    highlight_border=0.5,
                    h_align="center",
                    v_align="middle",
                    mouse_callbacks={"Button1": self._toggle_wifi_state},
                )
            )

        ########################################################
        ################### BLUETOOTH SECTION ##################
        ########################################################
        is_bt_enabled = bt_service.get_status()
        bt_section_pos_y = padding_y + section_height + margin_y + wlan_extra_height

        if is_bt_enabled:
            connected_devices = bt_service.get_connected_devices()

            controls.append(
                PopupText(
                    text="▼" if self.is_bt_list_expanded else "▶",
                    pos_x=padding_x,
                    pos_y=bt_section_pos_y,
                    width=icon_width,
                    height=section_height,
                    fontsize=12,
                    can_focus=True,
                    highlight=self.HIGHLIGHT_COLOR,
                    highlight_method="border",
                    highlight_border=0.5,
                    mouse_callbacks={"Button1": self._toggle_bt_list},
                    h_align="center",
                    v_align="middle",
                )
            )
            controls.append(
                PopupText(
                    text="󰂯",
                    pos_x=padding_x + icon_width + margin_x,
                    pos_y=bt_section_pos_y,
                    width=icon_width,
                    height=section_height,
                    fontsize=18,
                    can_focus=True,
                    highlight=self.HIGHLIGHT_COLOR,
                    highlight_method="border",
                    highlight_border=0.5,
                    h_align="center",
                    v_align="middle",
                    mouse_callbacks={"Button1": self._toggle_bt_state},
                )
            )
            if len(connected_devices) > 0:
                i = 0
                for mac in connected_devices:
                    controls.append(
                        PopupText(
                            text=f"{connected_devices[mac]["name"]} {connected_devices[mac]["battery"]}%",
                            pos_x=padding_x + 2 * icon_width + 2 * margin_x,
                            pos_y=bt_section_pos_y
                            + i * (list_margin_y + section_height),
                            width=popup_width
                            - (2 * padding_x + 2 * margin_x + 2 * icon_width),
                            height=section_height,
                            fontsize=16,
                            h_align="left",
                            v_align="middle",
                            can_focus=True,
                            highlight=self.HIGHLIGHT_COLOR,
                            highlight_method="border",
                            highlight_border=0.5,
                            mouse_callbacks={
                                "Button1": lambda q, m=mac: bt_service.disconnect_device(
                                    m
                                )
                            },
                        )
                    )
                    bt_connected_extra += i * (list_margin_y + section_height)
                    i += 1

            if self.is_bt_list_expanded:
                page_devices = []
                bt_list_pos_y = (
                    bt_section_pos_y
                    + section_height
                    + list_margin_y
                    + bt_connected_extra
                )

                if not self.available_bt_devices:
                    controls.append(
                        PopupText(
                            text="Scanning for Bluetooth devices...",
                            pos_x=padding_x + list_offset,
                            pos_y=bt_list_pos_y,
                            width=popup_width - 2 * padding_x - list_offset,
                            height=section_height,
                            fontsize=14,
                            h_align="left",
                            v_align="middle",
                        )
                    )
                if len(self.available_bt_devices) > 0:
                    start = self.bt_page * self.bt_items_per_page
                    end = start + self.bt_items_per_page
                    page_devices = self.available_bt_devices[start:end]

                    for i, device in enumerate(page_devices):
                        name = device.get("name", "Unknown")
                        mac = device["MAC"]
                        controls.append(
                            PopupText(
                                text=f"󰂱  {name}",
                                pos_x=padding_x + list_offset,
                                pos_y=bt_list_pos_y
                                + i * (section_height + list_margin_y),
                                width=popup_width - 2 * padding_x - list_offset,
                                height=section_height,
                                fontsize=14,
                                can_focus=True,
                                highlight=self.HIGHLIGHT_COLOR,
                                highlight_method="border",
                                highlight_border=0.5,
                                mouse_callbacks={
                                    "Button1": lambda q, m=mac: bt_service.connect_device(
                                        m
                                    ),
                                },
                            )
                        )

                    if self.bt_page > 0:
                        controls.append(
                            PopupText(
                                text="↑",
                                pos_x=popup_width - padding_x,
                                pos_y=bt_list_pos_y - 5,
                                width=20,
                                height=20,
                                fontsize=14,
                                can_focus=True,
                                highlight=self.HIGHLIGHT_COLOR,
                                highlight_method="border",
                                highlight_border=0.5,
                                mouse_callbacks={
                                    "Button1": lazy.function(self._prev_bt_page)
                                },
                            )
                        )
                    if len(self.available_bt_devices) > end:
                        controls.append(
                            PopupText(
                                text="↓",
                                pos_x=popup_width - padding_x,
                                pos_y=bt_list_pos_y
                                + self.bt_items_per_page * (section_height + padding_y),
                                width=20,
                                height=20,
                                fontsize=14,
                                can_focus=True,
                                highlight=self.HIGHLIGHT_COLOR,
                                highlight_method="border",
                                highlight_border=0.5,
                                mouse_callbacks={
                                    "Button1": lazy.function(self._next_bt_page)
                                },
                            )
                        )

        else:
            controls.append(
                PopupText(
                    text="󰂲",
                    pos_x=padding_x,
                    pos_y=bt_section_pos_y,
                    width=icon_width,
                    height=section_height,
                    fontsize=18,
                    can_focus=True,
                    highlight=self.HIGHLIGHT_COLOR,
                    highlight_method="border",
                    highlight_border=0.5,
                    h_align="center",
                    v_align="middle",
                    mouse_callbacks={"Button1": self._toggle_bt_state},
                )
            )

        ########################################################
        #################### VOLUME SECTION ####################
        ########################################################
        icons_section_pos_y = (
            bt_section_pos_y
            + section_height
            + margin_y
            + bt_extra_height
            + bt_connected_extra
        )
        value_section_pos_y = icons_section_pos_y + section_height + margin_y

        number_of_sections = 3
        section_width = (
            popup_width - (2 * padding_x + (number_of_sections - 1) * margin_x)
        ) / number_of_sections

        controls.append(
            PopupImage(
                filename=self.ASSETS_PATH + volume_filename,
                pos_x=padding_x,
                pos_y=icons_section_pos_y,
                width=section_width,
                height=section_height,
                mask=True,
                colour=self.MASK_COLOR,
                highlight=self.HIGHLIGHT_COLOR,
                highlight_method="border",
                highlight_border=0.5,
                h_align="center",
                v_align="center",
                mouse_callbacks={"Button1": self.volume_mute_toggle},
            ),
        )

        controls.append(
            PopupText(
                text=volume_text,
                pos_x=padding_x,
                pos_y=value_section_pos_y,
                width=section_width,
                height=section_height,
                fontsize=16,
                h_align="center",
                v_align="middle",
            )
        )

        ########################################################
        #################### MIC SECTION #######################
        ########################################################
        mic_section_pos_x = padding_x + section_width + margin_x

        controls.append(
            PopupImage(
                filename=self.ASSETS_PATH + mic_filename,
                pos_x=mic_section_pos_x,
                pos_y=icons_section_pos_y,
                width=section_width,
                height=section_height,
                mask=True,
                colour=self.MASK_COLOR,
                highlight=self.HIGHLIGHT_COLOR,
                highlight_method="border",
                highlight_border=0.5,
                h_align="center",
                v_align="center",
                mouse_callbacks={"Button1": self.mic_volume_mute_toggle},
            ),
        )

        controls.append(
            PopupText(
                text=mic_text,
                pos_x=mic_section_pos_x,
                pos_y=value_section_pos_y,
                width=section_width,
                height=section_height,
                fontsize=16,
                h_align="center",
                v_align="middle",
            )
        )

        ########################################################
        ################## BRIGHTNESS SECTION ##################
        ########################################################
        brightness_section_pos_x = mic_section_pos_x + section_width + margin_x
        brightness_filename = "brightness.svg"

        controls.append(
            PopupImage(
                filename=self.ASSETS_PATH + brightness_filename,
                pos_x=brightness_section_pos_x,
                pos_y=icons_section_pos_y,
                width=section_width,
                height=section_height,
                mask=True,
                can_focus=True,
                colour=self.MASK_COLOR,
                highlight=self.HIGHLIGHT_COLOR,
                highlight_method="border",
                highlight_border=0.5,
            ),
        )

        controls.append(
            PopupText(
                text=brightness_text,
                pos_x=brightness_section_pos_x,
                pos_y=value_section_pos_y,
                width=section_width,
                height=section_height,
                fontsize=16,
                h_align="center",
                v_align="middle",
            )
        )

        ########################################################
        #################### BATTERY SECTION ###################
        ########################################################
        bat_status = battery_service.get_status()
        bat_time = battery_service.get_time_remaining()
        bat_percent = battery_service.get_percent()
        bat_capacity = battery_service.get_capacity()

        bat_icon = next(f for level, f in self.battery_icon_map if bat_percent >= level)

        if bat_status == "Charging":
            bat_icon = ""

        second_icons_section_pos_y = value_section_pos_y + section_height + margin_y
        second_value_section_pos_y = second_icons_section_pos_y + section_height + 5

        number_of_sections = 2
        section_width = (
            popup_width - (2 * padding_x + (number_of_sections - 1) * margin_x)
        ) / number_of_sections

        controls.append(
            PopupText(
                text=f"{bat_icon}  {bat_percent}%",
                pos_x=padding_x,
                pos_y=second_icons_section_pos_y,
                width=section_width,
                height=section_height,
                mask=True,
                can_focus=True,
                colour=self.MASK_COLOR,
                highlight=self.HIGHLIGHT_COLOR,
                highlight_method="border",
                highlight_border=0.5,
                fontsize=16,
                h_align="center",
                v_align="middle",
            ),
        )

        controls.append(
            PopupText(
                text=f"{bat_time}  {bat_capacity}",
                pos_x=padding_x,
                pos_y=second_value_section_pos_y,
                width=section_width,
                height=section_height,
                fontsize=14,
                h_align="center",
                v_align="middle",
            )
        )

        ########################################################
        ################ AIRPLANE MODE SECTION #################
        ########################################################
        is_airplane_mode_enabled = airplane_mode_service.get_status()
        airplane_mode_text = "ON" if is_airplane_mode_enabled else "OFF"

        controls.append(
            PopupText(
                text="󰀝",
                pos_x=padding_x + section_width + margin_x,
                pos_y=second_icons_section_pos_y,
                width=section_width,
                height=section_height,
                mask=True,
                colour=self.MASK_COLOR,
                highlight=self.HIGHLIGHT_COLOR,
                highlight_method="border",
                highlight_border=0.5,
                fontsize=24,
                h_align="center",
                v_align="middle",
                mouse_callbacks={"Button1": self.airplane_mode_toggle},
            ),
        )

        controls.append(
            PopupText(
                text=airplane_mode_text,
                pos_x=padding_x + section_width + margin_x,
                pos_y=second_value_section_pos_y,
                width=section_width,
                height=section_height,
                fontsize=16,
                h_align="center",
                v_align="middle",
            )
        )

        popup_height = second_value_section_pos_y + section_height + padding_y

        self.layout = PopupAbsoluteLayout(
            qtile,
            width=popup_width,
            height=popup_height,
            controls=controls,
            initial_focus=self.focused_index,
            background=self.POPUP_COLOR,
            close_on_click=False,
        )

    def _next_wifi_page(self):
        self.wlan_page += 1
        self._refresh_layout()

    def _prev_wifi_page(self):
        if self.wlan_page > 0:
            self.wlan_page -= 1
        self._refresh_layout()

    def _next_bt_page(self):
        self.bt_page += 1
        self._refresh_layout()

    def _prev_bt_page(self):
        if self.bt_page > 0:
            self.bt_page -= 1
        self._refresh_layout()

    def volume_mute_toggle(self):
        self.focused_index = 4
        volume_service.toggle_mute()
        self._refresh_layout()

    def mic_volume_mute_toggle(self):
        self.focused_index = 5
        mic_service.toggle_mute()
        self._refresh_layout()

    def airplane_mode_toggle(self):
        self.focused_index = 8
        airplane_mode_service.toggle_airplane_mode(self.qtile)
        self._refresh_layout()

    def _toggle_wifi_state(self):
        self.focused_index = 1
        if self.is_wlan_list_expanded:
            self.is_wlan_list_expanded = False
        wlan_service.toggle_state(self.qtile)
        self._schedule_refresh(1.0)

    def _toggle_bt_state(self):
        self.focused_index = 3
        if self.is_bt_list_expanded:
            self.is_bt_list_expanded = False
        bt_service.toggle_state(self.qtile)
        self._schedule_refresh(1.0)

    def _toggle_wifi_list(self):
        self.focused_index = 0
        self.is_wlan_list_expanded = not self.is_wlan_list_expanded
        if self.is_wlan_list_expanded:
            self.available_networks = []

            def worker():
                nets = wlan_service.get_available_networks()
                self.available_networks = nets
                self._schedule_refresh()

            threading.Thread(target=worker, daemon=True).start()
        self._refresh_layout()

    def _toggle_bt_list(self):
        self.focused_index = 2
        self.is_bt_list_expanded = not self.is_bt_list_expanded
        if self.is_bt_list_expanded:
            self.available_bt_devices = []

            def worker():
                devices = (
                    bt_service.get_paired_devices()
                    + bt_service.get_discoverable_devices()
                )
                self.available_bt_devices = devices
                self._schedule_refresh()

            threading.Thread(target=worker, daemon=True).start()
        self._refresh_layout()

    def _schedule_refresh(self, delay=0.2):
        threading.Timer(
            delay,
            lambda: self.qtile.call_soon_threadsafe(lambda: self._refresh_layout()),
        ).start()

    def _refresh_layout(self):
        self._hide()
        self._show(self.qtile)

    def _show(self, qtile):
        self._create_layout(qtile)
        self.layout.show(centered=True)
        self.is_visible = True

    def _hide(self):
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
            self._hide()


menu_popup = MenuPopup()
