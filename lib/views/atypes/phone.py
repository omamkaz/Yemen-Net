#!/usr/bin/python3
# -*- coding: utf-8 -*-

import flet as ft
import requests
from ..card import Card
from ...scrapper import Phone
from ...constant import Dialogs
from ...models.user import User
from ..dialogs import CaptchaVerifyDialog


class PhoneCard(Card):
    def __init__(self, page: ft.Page, **kwargs):
        super().__init__(page, 2, **kwargs)

        self.card_credit.visible = False
        self._isp = Phone()

    def set_card_data(self) -> None:
        self.card_title.set_logo(self._user.atype)
        self.card_title.set_title(self._user.username)
        self.card_title.set_subtitle(self._user.dname)

        self.set_card_items(self._user.data)
        self.update()

    def login_web(self) -> None:
        self.card_title.set_loading(True)
        self._isp = Phone()

        try:
            self._isp.login(self._user.username)
            cv = CaptchaVerifyDialog(
                self.page, 
                self._isp,
                lambda data: self.on_captcha_verify_submit(data), 
                5
            )
            cv.open_dialog()
        except requests.exceptions.ConnectionError:
            # No Internet Connection
            Dialogs.no_internet_connection(self.page)
        except Exception as err:
            # Unknow Error!
            Dialogs.error(err)

        self.card_title.set_loading(False)

    def on_captcha_verify_submit(self, data: dict[str, str]) -> None:
        User.edit_data_and_cookies(self._user_id, data, None)
        self.set_card_data()

    @property
    def card_height(self) -> int:
        return 200
