#!/usr/bin/python3
# -*- coding: utf-8 -*-

import flet as ft
from ..card import Card
from ....scrapper import ADSL
from ....models.user import User
from ....constant import UserData
from ...dialogs import CaptchaVerifyDialog


class ADSLCard(Card):
    def __init__(self, page: ft.Page, **kwargs):
        super().__init__(page, 0, **kwargs)

        self._isp = ADSL()

    def set_card_data(self, old_data: dict[str, str] = None) -> None:
        pdata = UserData.filter_data(self._user.data.copy(), self._user.atype)

        self.card_title.set_logo(self._user.atype)
        self.card_title.set_subtitle(self._user.username)

        self.card_title.set_title(pdata.pop("name"))
        self.card_title.set_active(pdata.pop("account_status"))
        self.card_credit.set_credit(pdata.pop("valid_credit"))
        self.card_credit.set_credit_state(self._user.data, old_data)

        self.set_card_items(pdata)
        self.update()

    def fetch_web_data(self) -> None:
        old_data = self._user.data.copy() if self._user.data else None
        new_data = self._isp.fetch_data(self._user.cookies)

        User.edit_data_and_cookies(self._user_id, new_data, self._isp.get_cookies())
        self.set_card_data(old_data)

    def start_captcha_verify(self) -> None:
        old_data = self._user.data.copy() if self._user.data else None

        self._isp.login(self._user.username, self._user.password)
        cv = CaptchaVerifyDialog(
            self.page, 
            self._isp, 
            lambda data: self.on_captcha_verify_submit(data, old_data),
            4
        )
        cv.open_dialog()

    def login_web(self) -> None:
        self._isp = ADSL()
        self.fetch_web_data()

    def on_captcha_verify_submit(self, data: dict[str, str], old_data: dict[str, str]) -> None:
        super().on_captcha_verify_submit(0, data, old_data, self._isp.get_cookies())