from libqtile.lazy import lazy
from qtile_extras.popup import PopupAbsoluteLayout, PopupText, PopupImage, PopupWidget
from qtile_extras import widget
import threading
import subprocess

from ..variables import BAR_FOREGROUND, BAR_BACKGROUND, ASSETS_PATH, HIGH_DPI_MULTIPLIER
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
        assets_path=ASSETS_PATH,
    ):
        self.layout = None
        self.qtile = None
        self.is_visible = False
        self.available_networks = []
        self.wlan_page = 0
        self.wlan_items_per_page = 4
        self.bt_items_per_page = 4
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

    def _disconnect_bt_device(self, mac):
        bt_service.disconnect_device(mac)
        self._schedule_refresh()

    def _disconnect_current_network(self):
        wlan_service.disconnect_from_network()
        self._schedule_refresh()

    def _connect_to_bt_device(self, mac):
        bt_service.connect_device(mac)
        self._schedule_refresh()

    def _connect_to_network(self, ssid, security):
        result = wlan_service.connect_to_network(ssid)
        if result:
            self._schedule_refresh()
            return
        sec = (security or "").upper()
        if any(x in sec for x in ("WPA", "WEP", "PSK")):
            self._ask_password_for_ssid(ssid)
        else:
            try:
                wlan_service.connect_to_network(ssid)
            except Exception as e:
                print("WiFi connect error:", e)
            self._schedule_refresh()

    def _ask_password_for_ssid(self, ssid):
        def worker():
            try:
                result = subprocess.run(
                    ["rofi", "-dmenu", "-password", "-p", f"Hasło do {ssid}:"],
                    capture_output=True,
                    text=True,
                )
                password = result.stdout.strip()
                if password:
                    try:
                        wlan_service.connect_to_network(ssid, password=password)
                    except TypeError:
                        wlan_service.connect_to_network(ssid, password)
                self._schedule_refresh()
            except Exception as e:
                print("Password prompt error:", e)

        threading.Thread(target=worker, daemon=True).start()

    def _create_layout(self, qtile, focused_index=0):
        self.qtile = qtile
        controls = []

        volume_text, volume_filename = self._get_volume_data()
        mic_text, mic_filename = self._get_mic_data()
        brightness_text = self._get_brightness_data()

        icon_width = int(25 * HIGH_DPI_MULTIPLIER)
        list_offset = int(40 * HIGH_DPI_MULTIPLIER)
        image_height = int(30 * HIGH_DPI_MULTIPLIER)
        section_height = image_height
        text_width = 70
        margin_x = int(10 * HIGH_DPI_MULTIPLIER)
        margin_y = int(20 * HIGH_DPI_MULTIPLIER)
        list_margin_y = int(5 * HIGH_DPI_MULTIPLIER)
        padding_y = int(20 * HIGH_DPI_MULTIPLIER)
        padding_x = int(20 * HIGH_DPI_MULTIPLIER)
        popup_width = int(400 * HIGH_DPI_MULTIPLIER)
        bt_extra_height = self._calculate_bt_extra_height(section_height)
        wlan_extra_height = self._calculate_wlan_extra_height(section_height)
        bt_connected_extra = 0

        controls.append(
            PopupWidget(
                widget=widget.Clock(
                    format="%H:%M:%S %d.%m.%Y", fontsize=int(25 * HIGH_DPI_MULTIPLIER)
                ),
                pos_x=popup_width // 2 - int(300 * HIGH_DPI_MULTIPLIER) // 2,
                pos_y=padding_y,
                width=int(300 * HIGH_DPI_MULTIPLIER),
                height=section_height,
                h_align="center",
                v_align="middle",
            ),
        )

        ########################################################
        ###################### WLAN SECTION ####################
        ########################################################
        is_wifi_enabled = wlan_service.get_status()
        wlan_section_pos_y = padding_y + section_height + margin_y

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
                    pos_y=wlan_section_pos_y,
                    width=icon_width,
                    height=section_height,
                    fontsize=int(12 * HIGH_DPI_MULTIPLIER),
                    can_focus=True,
                    foreground=self.TEXT_COLOR,
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
                    pos_y=wlan_section_pos_y,
                    width=icon_width,
                    height=section_height,
                    fontsize=int(18 * HIGH_DPI_MULTIPLIER),
                    can_focus=True,
                    foreground=self.TEXT_COLOR,
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
                    pos_y=wlan_section_pos_y,
                    width=(popup_width - 2 * padding_x - 2 * margin_x - 2 * icon_width)
                    / 2,
                    height=section_height,
                    fontsize=int(16 * HIGH_DPI_MULTIPLIER),
                    can_focus=True,
                    foreground=self.TEXT_COLOR,
                    highlight=self.HIGHLIGHT_COLOR,
                    highlight_method="border",
                    highlight_border=0.5,
                    h_align="center",
                    v_align="middle",
                    mouse_callbacks={"Button1": self._disconnect_current_network},
                )
            )
            controls.append(
                PopupText(
                    text=ip_address,
                    pos_x=padding_x
                    + 2 * icon_width
                    + 3 * margin_x
                    + (popup_width - 2 * padding_x - 2 * margin_x - 2 * icon_width) / 2,
                    pos_y=wlan_section_pos_y,
                    width=(popup_width - 2 * padding_x - 3 * margin_x - 2 * icon_width)
                    / 2,
                    height=section_height,
                    foreground=self.TEXT_COLOR,
                    fontsize=int(16 * HIGH_DPI_MULTIPLIER),
                    h_align="center",
                    v_align="middle",
                )
            )

            if self.is_wlan_list_expanded:
                wlan_list_pos_y = wlan_section_pos_y + section_height + list_margin_y

                if not self.available_networks:
                    controls.append(
                        PopupText(
                            text="Scanning for Wi-Fi...",
                            pos_x=padding_x + list_offset,
                            pos_y=wlan_list_pos_y,
                            width=popup_width - 2 * padding_x - 40,
                            height=section_height,
                            fontsize=int(14 * HIGH_DPI_MULTIPLIER),
                            foreground=self.TEXT_COLOR,
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
                                fontsize=int(14 * HIGH_DPI_MULTIPLIER),
                                can_focus=True,
                                foreground=self.TEXT_COLOR,
                                highlight=self.HIGHLIGHT_COLOR,
                                highlight_method="border",
                                highlight_border=0.5,
                                mouse_callbacks={
                                    "Button1": (
                                        lambda s=ssid, sec=security: self._connect_to_network(
                                            s, sec
                                        )
                                    )
                                },
                            )
                        )

                    if self.wlan_page > 0:
                        controls.append(
                            PopupText(
                                text="",
                                pos_x=padding_x,
                                pos_y=wlan_list_pos_y,
                                width=20,
                                height=20,
                                fontsize=int(14 * HIGH_DPI_MULTIPLIER),
                                can_focus=True,
                                foreground=self.TEXT_COLOR,
                                highlight=self.HIGHLIGHT_COLOR,
                                highlight_method="border",
                                highlight_border=0.5,
                                mouse_callbacks={"Button1": self._prev_wifi_page},
                                h_align="center",
                                v_align="middle",
                            )
                        )
                    if len(self.available_networks) > end:
                        controls.append(
                            PopupText(
                                text="",
                                pos_x=padding_x,
                                pos_y=wlan_list_pos_y + 25,
                                width=20,
                                height=20,
                                fontsize=int(14 * HIGH_DPI_MULTIPLIER),
                                can_focus=True,
                                foreground=self.TEXT_COLOR,
                                highlight=self.HIGHLIGHT_COLOR,
                                highlight_method="border",
                                highlight_border=0.5,
                                mouse_callbacks={"Button1": self._next_wifi_page},
                                h_align="center",
                                v_align="middle",
                            )
                        )
        else:
            controls.append(
                PopupText(
                    text="󰤭",
                    pos_x=padding_x,
                    pos_y=wlan_section_pos_y,
                    width=popup_width - 2 * padding_x,
                    height=section_height,
                    fontsize=int(18 * HIGH_DPI_MULTIPLIER),
                    can_focus=True,
                    foreground=self.TEXT_COLOR,
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
        bt_section_pos_y = (
            wlan_section_pos_y + section_height + margin_y + wlan_extra_height
        )

        if is_bt_enabled:
            connected_devices = bt_service.get_connected_devices()

            controls.append(
                PopupText(
                    text="▼" if self.is_bt_list_expanded else "▶",
                    pos_x=padding_x,
                    pos_y=bt_section_pos_y,
                    width=icon_width,
                    height=section_height,
                    fontsize=int(12 * HIGH_DPI_MULTIPLIER),
                    can_focus=True,
                    foreground=self.TEXT_COLOR,
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
                    fontsize=int(18 * HIGH_DPI_MULTIPLIER),
                    can_focus=True,
                    foreground=self.TEXT_COLOR,
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
                            text=f"{connected_devices[mac]["name"]} - {connected_devices[mac]["battery"]}%",
                            pos_x=padding_x + 2 * icon_width + 2 * margin_x,
                            pos_y=bt_section_pos_y
                            + i * (list_margin_y + section_height),
                            width=popup_width
                            - (2 * padding_x + 2 * margin_x + 2 * icon_width),
                            height=section_height,
                            fontsize=int(16 * HIGH_DPI_MULTIPLIER),
                            h_align="center",
                            v_align="middle",
                            can_focus=True,
                            foreground=self.TEXT_COLOR,
                            highlight=self.HIGHLIGHT_COLOR,
                            highlight_method="border",
                            highlight_border=0.5,
                            mouse_callbacks={
                                "Button1": lambda m=mac: self._disconnect_bt_device(m)
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
                            fontsize=int(14 * HIGH_DPI_MULTIPLIER),
                            foreground=self.TEXT_COLOR,
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
                                fontsize=int(14 * HIGH_DPI_MULTIPLIER),
                                can_focus=True,
                                foreground=self.TEXT_COLOR,
                                highlight=self.HIGHLIGHT_COLOR,
                                highlight_method="border",
                                highlight_border=0.5,
                                mouse_callbacks={
                                    "Button1": lambda m=mac: self._connect_to_bt_device(
                                        m
                                    ),
                                },
                            )
                        )

                    if self.bt_page > 0:
                        controls.append(
                            PopupText(
                                text="",
                                pos_x=padding_x,
                                pos_y=bt_list_pos_y,
                                width=20,
                                height=20,
                                fontsize=int(14 * HIGH_DPI_MULTIPLIER),
                                can_focus=True,
                                foreground=self.TEXT_COLOR,
                                highlight=self.HIGHLIGHT_COLOR,
                                highlight_method="border",
                                highlight_border=0.5,
                                mouse_callbacks={"Button1": self._prev_bt_page},
                                h_align="center",
                                v_align="middle",
                            )
                        )
                    if len(self.available_bt_devices) > end:
                        controls.append(
                            PopupText(
                                text="",
                                pos_x=padding_x,
                                pos_y=bt_list_pos_y + 25,
                                width=20,
                                height=20,
                                fontsize=int(14 * HIGH_DPI_MULTIPLIER),
                                can_focus=True,
                                foreground=self.TEXT_COLOR,
                                highlight=self.HIGHLIGHT_COLOR,
                                highlight_method="border",
                                highlight_border=0.5,
                                mouse_callbacks={"Button1": self._next_bt_page},
                                h_align="center",
                                v_align="middle",
                            )
                        )

        else:
            controls.append(
                PopupText(
                    text="󰂲",
                    pos_x=padding_x,
                    pos_y=bt_section_pos_y,
                    width=popup_width - 2 * padding_x,
                    height=section_height,
                    fontsize=int(18 * HIGH_DPI_MULTIPLIER),
                    can_focus=True,
                    foreground=self.TEXT_COLOR,
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
                fontsize=int(16 * HIGH_DPI_MULTIPLIER),
                foreground=self.TEXT_COLOR,
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
                fontsize=int(16 * HIGH_DPI_MULTIPLIER),
                foreground=self.TEXT_COLOR,
                h_align="center",
                v_align="middle",
            )
        )

        ########################################################
        ################ AIRPLANE MODE SECTION #################
        ########################################################
        is_airplane_mode_enabled = airplane_mode_service.get_status()
        airplane_mode_text = "ON" if is_airplane_mode_enabled else "OFF"

        airplane_mode_section_pos_x = mic_section_pos_x + section_width + margin_x
        controls.append(
            PopupText(
                text="󰀝",
                pos_x=airplane_mode_section_pos_x,
                pos_y=icons_section_pos_y,
                width=section_width,
                height=section_height,
                mask=True,
                foreground=self.TEXT_COLOR,
                highlight=self.HIGHLIGHT_COLOR,
                highlight_method="border",
                highlight_border=0.5,
                fontsize=int(30 * HIGH_DPI_MULTIPLIER),
                h_align="center",
                v_align="middle",
                mouse_callbacks={"Button1": self.airplane_mode_toggle},
            ),
        )

        controls.append(
            PopupText(
                text=airplane_mode_text,
                pos_x=airplane_mode_section_pos_x,
                pos_y=value_section_pos_y,
                width=section_width,
                height=section_height,
                fontsize=int(16 * HIGH_DPI_MULTIPLIER),
                foreground=self.TEXT_COLOR,
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
                can_focus=False,
                foreground=self.TEXT_COLOR,
                highlight=self.HIGHLIGHT_COLOR,
                highlight_method="border",
                highlight_border=0.5,
                fontsize=int(16 * HIGH_DPI_MULTIPLIER),
                h_align="center",
                v_align="middle",
            ),
        )

        controls.append(
            PopupText(
                text=f"{bat_time if len(bat_time)>0 else ''}   {bat_capacity}",
                pos_x=padding_x,
                pos_y=second_value_section_pos_y,
                width=section_width,
                height=section_height,
                fontsize=int(14 * HIGH_DPI_MULTIPLIER),
                foreground=self.TEXT_COLOR,
                h_align="center",
                v_align="middle",
            )
        )

        ########################################################
        ################## BRIGHTNESS SECTION ##################
        ########################################################
        brightness_filename = "brightness.svg"

        controls.append(
            PopupImage(
                filename=self.ASSETS_PATH + brightness_filename,
                pos_x=padding_x + section_width + margin_x,
                pos_y=second_icons_section_pos_y,
                width=section_width,
                height=section_height,
                mask=True,
                can_focus=False,
                colour=self.MASK_COLOR,
                highlight=self.HIGHLIGHT_COLOR,
                highlight_method="border",
                highlight_border=0.5,
            ),
        )

        controls.append(
            PopupText(
                text=brightness_text,
                pos_x=padding_x + section_width + margin_x,
                pos_y=second_value_section_pos_y,
                width=section_width,
                height=section_height,
                fontsize=int(16 * HIGH_DPI_MULTIPLIER),
                foreground=self.TEXT_COLOR,
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
            initial_focus=focused_index,
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
        volume_service.toggle_mute()
        self._refresh_layout()

    def mic_volume_mute_toggle(self):
        mic_service.toggle_mute()
        self._refresh_layout()

    def airplane_mode_toggle(self):
        airplane_mode_service.toggle_airplane_mode(self.qtile)
        self._refresh_layout()

    def _toggle_wifi_state(self):
        if self.is_wlan_list_expanded:
            self.is_wlan_list_expanded = False
        wlan_service.toggle_state(self.qtile)
        self._schedule_refresh(1.0)

    def _toggle_bt_state(self):
        if self.is_bt_list_expanded:
            self.is_bt_list_expanded = False
        bt_service.toggle_state(self.qtile)
        self._schedule_refresh(1.0)

    def _toggle_wifi_list(self):
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
        self.is_bt_list_expanded = not self.is_bt_list_expanded
        if self.is_bt_list_expanded:
            self.available_bt_devices = []

            def worker():
                devices = bt_service.get_discoverable_devices()
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
        focused_index = 0
        if self.layout and self.layout._focused is not None:
            focused_index = self.layout.focusable_controls.index(self.layout._focused)
        self.hide()
        self._show(self.qtile, focused_index)

    def _show(self, qtile, focused_index=0):
        self._create_layout(qtile, focused_index)
        self.layout.show(relative_to=2, relative_to_bar=True)
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


menu_popup = MenuPopup()
