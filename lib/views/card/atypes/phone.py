#!/usr/bin/python3
# -*- coding: utf-8 -*-

import flet as ft
from ..card import Card
from ....scrapper import Phone
from ...dialogs import CaptchaVerifyDialog


class PhoneCard(Card):
    def __init__(self, page: ft.Page, **kwargs):
        super().__init__(page, 2, **kwargs)

        self.card_credit.visible = False
        self._isp = Phone()

    def set_card_data(self, old_data: dict[str, str] = None) -> None:
        self.card_title.set_logo(self._user.atype)
        self.card_title.set_title(self._user.username)
        self.card_title.set_subtitle(self._user.dname)

        self.set_card_items(self._user.data)
        self.update()

    def start_captcha_verify(self) -> None:
        self._isp.login(self._user.username)
        cv = CaptchaVerifyDialog(
            self.page,
            self._isp,
            lambda data: self.on_captcha_verify_submit(data),
            5
        )
        cv.open_dialog()

    def login_web(self) -> None:
        self._isp = Phone()
        self.start_captcha_verify()

    def on_captcha_verify_submit(self, data: dict[str, str]) -> None:
        super().on_captcha_verify_submit(2, data, None, None)

    @property
    def card_height(self) -> int:
        return 200
