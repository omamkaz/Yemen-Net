#!/usr/bin/python3
# -*- coding: utf-8 -*-

import flet as ft
import requests
from .card import Card
from ..models.user import User
from ..constant import UserData, Dialogs
from ..scrapper import ADSL, LTE, Phone
from .captcha_verify import CaptchaVerify


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

        self.set_card_items(pdata)

        if old_data:
            self.card_credit.set_credit_state(self._user.data, old_data)

        self.update()

    def fetch_web_data(self) -> None:
        self.card_title.set_loading(True)

        old_data = self._user.data.copy() if self._user.data is not None else {}
        new_data = self._isp.fetch_data(self._user.cookies)

        User.edit_data_and_cookies(self._user_id, new_data, self._isp.get_cookies())
        self.set_card_data(old_data)

        self.card_title.set_loading(False)

    def start_captcha_verify(self) -> None:
        self._isp.login(self._user.username, self._user.password)
        cv = CaptchaVerify(self.page, self._isp, self.on_captcha_verify_submit, 4)
        cv.open_dialog()

    def login_web(self) -> None:
        self.card_title.set_loading(True)

        try:
            self.fetch_web_data()
        except AttributeError:
            self.start_captcha_verify()
        except requests.exceptions.ConnectionError:
            # No Internet Connection
            Dialogs.no_internet_connection(self.page)
        except Exception as err:
            # Unknow Error!
            Dialogs.error(err)

        self.card_title.set_loading(False)

    def on_captcha_verify_submit(self, data: dict[str, str], old_data: dict[str, str] = None) -> None:
        User.edit_data_and_cookies(self._user_id, data, self._isp.get_cookies())
        self.set_card_data(old_data)


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

        self.set_card_items(pdata)

        if old_data:
            self.card_credit.set_credit_state(self._user.data, old_data)

        self.update()

    def login_web(self) -> None:
        self.card_title.set_loading(True)

        try:
            old_data = self._user.data
            self._isp.login(self._user.username)

            cv = CaptchaVerify(
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

    def on_captcha_verify_submit(self, data: dict[str, str], old_data: dict[str, str] = None) -> None:
        User.edit_data_and_cookies(self._user_id, data, None)
        self.set_card_data(old_data)


class PhoneCard(Card):
    def __init__(self, page: ft.Page, **kwargs):
        super().__init__(page, 2, **kwargs)

        self.content.height = 200
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

        try:
            self._isp.login(self._user.username)
            cv = CaptchaVerify(
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
