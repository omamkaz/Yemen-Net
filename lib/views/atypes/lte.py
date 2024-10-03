#!/usr/bin/python3
# -*- coding: utf-8 -*-

import flet as ft
import requests
from ..card import Card
from ...scrapper import LTE
from ...models.user import User
from ...constant import UserData, Dialogs
from ..dialogs import CaptchaVerifyDialog


class LTECard(Card):
    def __init__(self, page: ft.Page, **kwargs):
        super().__init__(page, 1, **kwargs)
        self._isp = LTE()

    def set_card_data(self, old_data: dict[str, str] = None) -> None:

        pdata = UserData.filter_data(self._user.data.copy(), self._user.atype)

        self.card_title.set_title(self._user.username)
        self.card_title.set_subtitle(self._user.dname)
        self.card_title.set_logo(self._user.atype)
        self.card_credit.set_credit(pdata.pop("valid_credit"))
        self.card_credit.set_credit_state(self._user.data, old_data)

        self.set_card_items(pdata)
        self.update()

    def login_web(self) -> None:
        self.card_title.set_loading(True)
        self._isp = LTE()

        try:
            old_data = self._user.data.copy() if self._user.data else None
            self._isp.login(self._user.username)

            cv = CaptchaVerifyDialog(
                self.page, 
                self._isp, 
                lambda data: self.on_captcha_verify_submit(data, old_data), 
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

    def on_captcha_verify_submit(
            self, 
            data: dict[str, str], 
            old_data: dict[str, str] = None) -> None:
        User.edit_data_and_cookies(self._user_id, data, None)
        self.set_card_data(old_data)
