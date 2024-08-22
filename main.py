#!/usr/bin/python3
# -*- coding: utf-8 -*-

import requests
import humanize
import flet as ft

from datetime import datetime
from lib.view.card import YCard
from lib.view.new_account_dialog import YNewAccountDialog
from lib.view.theme_dialog import YThemeModeSelect
from lib.view.captcha_verify_dialog import YCaptchaVerifyDialog
from lib.view.list_item import YListItem
from lib.model.client_storage import ClientStorage
from lib.yadsl import YADSL


class YNoInternetConnectionDialog(ft.AlertDialog):
    def __init__(self):
        super().__init__()

        self.title = ft.Text(
            value = "لايوجد اتصال باالانترنت!",
            text_align="center"
        )
        self.icon = ft.Icon(
            name = ft.icons.WIFI_OFF,
            size = 32
        )


class MainWindow:
    def __init__(self, page: ft.Page):
        self._page = page

        self.yn = YADSL()

        self.card_title = ft.Ref[ft.Text]()
        self.last_check_time = ft.Ref[ft.Text]()

        self.client_storage = ClientStorage(page)
        self.theme_mode_select = YThemeModeSelect(page)

        self.card = YCard()
        self.dialog = YNewAccountDialog(page)
        self.captcha_dialog = YCaptchaVerifyDialog(page)

        self.captcha_dialog.captcha_update.current.on_click = self.handle_captcha_update

        for a in self.dialog.actions:
            a.on_click = self.handle_close

        self.recent_user = ft.ListView(
            expand=1,
            spacing=6,
            padding=ft.padding.only(6, 6, 0, 6), # b:25
            controls=[
                self.list_item(atype, username)
                for atype, username in self.client_storage.get_users()
            ]
        )

    def list_item(self, atype: int, username: str) -> YListItem:
        return YListItem(
            atype, 
            username,
            self.client_storage,
            self.handle_item_click, 
            self.handle_item_long_press,
            self.handle_item_delete_click
        )

    def add_new_item(self, atype: int | str, username: str):
        self.recent_user.controls.append(self.list_item(atype, username))
        self.recent_user.update()

    def handle_item_long_press(self, e: ft.ControlEvent):
        for c in self.recent_user.controls:
            c.trailing.visible = False
        e.control.trailing.visible = True
        self.recent_user.update()

    def handle_item_click(self, e: ft.ControlEvent):
        for c in self.recent_user.controls:
            c.trailing.visible = False
        self.recent_user.update()

        atype, username = e.control.data

        self.card_title.current.value = e.control.title.value
        self.card_title.current.update()

        if (user_data := self.client_storage.get_user_data_key(atype, username, "data")):
            self.card.set_data(atype, username, user_data)
            _datetime = self.client_storage.get_user_data_key(atype, username, "last_check")
            self.last_check_time.current.value = humanize.naturaltime(datetime.fromtimestamp(_datetime)) if _datetime is not None else ""
            self.last_check_time.current.update()
        else:
            self.login_wizard(atype, username)

    def login_wizard(self, atype, username):
        self.yn = YADSL()

        password = self.client_storage.get_user_data_key(atype, username, "password")
        self.yn.login(username, password)

        captcha_image = self.yn.fetch_captcha()
        self.captcha_dialog.actions[0].on_click = lambda e: self.handle_captcha_verify(atype, username)
        self.captcha_dialog.open_dialog(atype, username, captcha_image)

    def handle_captcha_update(self, e: ft.ControlEvent):
        self.captcha_dialog.set_captcha_image(self.yn.fetch_captcha())
        self.captcha_dialog.update()

    def handle_captcha_verify(self, atype: int | str, username: str):
        _, err = self.yn.verify(self.captcha_dialog.captcha_value.value)

        if err is not None:
            dialog = ft.AlertDialog(
                icon = ft.Icon(
                    name = ft.icons.ERROR,
                    color = ft.colors.RED_500,
                    size = 32
                ),
                title = ft.Text(
                    value = err,
                    text_align="center"
                )
            )
            self._page.open(dialog)
        else:
            new_data = self.yn.fetch_data()
            prev_data = self.client_storage.get_user_data_key(atype, username, "data")

            self.card.set_data(
                atype, 
                username, 
                new_data,
                prev_data
            )
            self.last_check_time.current.value = humanize.naturaltime(datetime.now())
            self.last_check_time.current.update()

            self.client_storage.update_user_data_key(atype, username, "data", new_data)
            self.client_storage.update_user_data_key(atype, username, "cookies", self.yn.get_cookies())
            self.client_storage.update_user_data_key(atype, username, "last_check", datetime.now().timestamp())

            self._page.close(self.captcha_dialog)

    def handle_item_delete_click(self, e: ft.ControlEvent):
        atype, username = e.control.data

        for c in self.recent_user.controls:
            if str(c.data[0]) == str(atype) and c.data[1] == username:
                self.recent_user.controls.remove(c)

        self.client_storage.remove_user(atype, username)
        self.recent_user.update()
        self.card.clear_card()
        self.card_title.current.value = ""
        self.card_title.current.update()

    def handle_close(self, e: ft.ControlEvent) -> None:
        atype = self.dialog._index
        display_name = self.dialog.display_name.value.strip()
        username = self.dialog.username.value.strip()

        if e.control.data == 0:
            self._page.close(self.dialog)
            self.dialog.username.error_text = None

        elif not username:
            self.dialog.username.error_text = "ادخل اسم المستخدم"

        elif self.client_storage.is_exists(atype, username):
            self.dialog.username.error_text = "اسم المستخدم موجود!"

        elif e.control.data == 1 and username:
            info = {
                "name": display_name,
                "password": self.dialog.password.value.strip() or "123456"
            }

            self.client_storage.add_user(atype, username, info)
            self.add_new_item(atype, username)
            self.dialog.clear_forms()

            self._page.close(self.dialog)
            self.dialog.username.error_text = None

        self.dialog.update()

    # def handle_search_item(self, e: ft.ControlEvent):
    #     for c in self.recent_user.controls:
    #         username = c.data[1]
    #         name = self.client_storage.get_user_data_key(*c.data, "name") or ""
    #         value = e.control.value.strip()
    #         c.visible = value in username or value in name

    #     self.recent_user.update()
    #     self._page.update()

    def build(self) -> list[ft.Control]:
        return [
            self.card,
            ft.Container(
                content=ft.Row(
                    controls=[
                        ft.Text(
                            ref = self.last_check_time,
                            size = 13, 
                            text_align="center",
                            font_family="Cairo"
                        ),
                        ft.Text(
                            ref = self.card_title,
                            size = 18,
                            text_align="center",
                            font_family="ElMessiri"
                        )
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER
                ),
            ),
            # ft.TextField(
            #     text_align="center",
            #     on_change=self.handle_search_item
            # ),
            self.recent_user,
            ft.Container(
                border_radius=10,
                bgcolor=ft.colors.AMBER_400,
                shadow = ft.BoxShadow(
                    # spread_radius=0.7,
                    blur_radius=4
                ),
                content=ft.Row(
                    controls = [
                        ft.IconButton(
                            icon_color = ft.colors.BROWN,
                            icon=ft.icons.DARK_MODE,
                            on_click=lambda e: self._page.open(self.theme_mode_select),
                        ),
                        ft.IconButton(
                            icon_color = ft.colors.BROWN,
                            icon=ft.icons.REFRESH,
                            on_click=self.on_refresh_user
                        ),
                        ft.IconButton(
                            icon_color = ft.colors.BROWN,
                            icon=ft.icons.ADD,
                            on_click=self.on_add_user
                        )
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_EVENLY
                )
            ),
            ## About Creator
            ft.Row(
                controls=[
                    ft.Text(
                        value = "v2.0.0",
                        size = 10,
                        text_align="left"
                    ),
                    ft.Text(
                        spans=[
                            ft.TextSpan(
                                text = "تم الانشاء بواسطة: ",
                                style = ft.TextStyle(
                                    size=10,
                                    font_family="Cairo"
                                )
                            ),
                            ft.TextSpan(
                                text = "أسامة الزبيدي",
                                style = ft.TextStyle(
                                    size=11, 
                                    letter_spacing=2,
                                    weight=ft.FontWeight.BOLD,
                                    font_family="ElMessiri"
                                )
                            )
                        ],
                        selectable=True
                    )
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN
            )
        ]

    def on_refresh_user(self, e: ft.ControlEvent):
        atype = self.card._atype
        username = self.card._username

        if atype and username:
            try:
                cookies = self.client_storage.get_user_data_key(atype, username, "cookies")
                prev_data = self.client_storage.get_user_data_key(atype, username, "data")

                new_data = self.yn.fetch_data(cookies)

                self.card.set_data(atype, username, new_data, prev_data)
                self.last_check_time.current.value = humanize.naturaltime(datetime.now())
                self.last_check_time.current.update()

                self.client_storage.update_user_data_key(atype, username, "data", new_data)
                self.client_storage.update_user_data_key(atype, username, "last_check", datetime.now().timestamp())

            except requests.exceptions.ConnectionError: # no internet connection
                dialog = YNoInternetConnectionDialog()
                self._page.open(dialog)
            except AttributeError: # session end
                self.login_wizard(atype, username)

    def on_add_user(self, e: ft.ControlEvent) -> None:
        self._page.open(self.dialog)



def main(page: ft.Page):
    page.fonts = {
        "ElMessiri": "fonts/ElMessiri-Regular.ttf",
        "Beiruti": "fonts/Beiruti-Regular.ttf",
        "Cairo": "fonts/Cairo-Regular.ttf"
    }

    theme_mode: str = page.client_storage.get("theme.mode") or "system"
    page.theme_mode = ft.ThemeMode(theme_mode)

    theme_color = ft.colors.AMBER_ACCENT
    page.theme = ft.Theme(
        primary_color = theme_color,
        color_scheme_seed=theme_color,
        card_theme=ft.CardTheme(
            color = theme_color
        )
    )

    # page.window.wait_until_ready_to_show = True
    # page.window.width = 300
    # page.window.height = 600

    page.window.icon = "assets/icon.png"
    page.title = "Yemen Net (omamkaz)"
    page.vertical_alignment = "center"
    page.horizontal_alignment = "center"

    window = MainWindow(page)
    page.add(*window.build())

if __name__ == "__main__":
    ft.app(
        target=main, 
        name="yemen_net"
    )