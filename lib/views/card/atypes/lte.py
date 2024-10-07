#!/usr/bin/python3
# -*- coding: utf-8 -*-

import flet as ft
from ..card import Card
from ....scrapper import LTE
from ....constant import UserData
from ...dialogs import CaptchaVerifyDialog


class LTECard(Card):
    def __init__(self, page: ft.Page, **kwargs):
        super().__init__(page, 1, **kwargs)

        self._isp = LTE()

    def set_card_data(self, old_data: dict[str, str] = None) -> None:
        pdata = UserData.filter_data(self._user.data.copy(), self._user.atype)

        self.card_title.set_logo(self._user.atype)
        self.card_title.set_title(self._user.username)
        self.card_title.set_subtitle(self._user.dname)
        self.card_credit.set_credit(pdata.pop("valid_credit"))
        self.card_credit.set_credit_state(self._user.data, old_data)

        self.set_card_items(pdata)
        self.update()

    def start_captcha_verify(self) -> None:
        old_data = self._user.data.copy() if self._user.data else None
        self._isp.login(self._user.username)
        cv = CaptchaVerifyDialog(
            self.page, 
            self._isp, 
            lambda data: self.on_captcha_verify_submit(data, old_data), 
            5
        )
        cv.open_dialog()

    def login_web(self) -> None:
        self._isp = LTE()
        self.start_captcha_verify()

    def on_captcha_verify_submit(self, data: dict[str, str], old_data: dict[str, str] = None) -> None:
        super().on_captcha_verify_submit(1, data, old_data, None)
