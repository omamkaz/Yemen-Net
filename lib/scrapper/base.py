#!/usr/bin/python3
# -*- coding: utf-8 -*-

import random
import requests
from typing import Any
from bs4 import BeautifulSoup


class ParserError(Exception):
    def __init__(self, err: str):
        super().__init__(err)


class Erros:
    @classmethod
    def err(cls, resp: requests.Response, err_id: str) -> str | None: # if the return is None that means doesn't have any error!
        soup = Base.bs4(resp)

        # phone number error
        if (label := soup.find("label", id=err_id)) is not None and label.text.strip():
            return label.text.strip()

        # captcha error
        if (span := soup.find("span", class_="error")) is not None:
            return span.text.strip()

        # No Data error
        if (p := soup.find("p", id="pmsgerr")) is not None and (err := p.find("font").text.strip()):
            return err


class Payload:
    def __init__(self):
        self._data = {}

        self.username: str = None
        self.captcha: str = None

    def set_username(self, username: str) -> None:
        self._data[self.username] = username

    def set_captcha(self, captcha: str) -> None:
        self._data[self.captcha] = captcha

    def set(self, key: str, value: Any) -> None:
        self._data[key] = value

    @property
    def data(self) -> dict:
        return self._data


class Base:
    def __init__(self):
        self._payload: Payload = Payload()
        self._login_url: str = ""
        self._captcha_url: str = ""
        self._timeout: int = 10
        self.init_session()

    @staticmethod
    def bs4(req: requests.Request) -> BeautifulSoup:
        return BeautifulSoup(req.content, "html.parser")

    def init_session(self):
        self._session = requests.Session()

    def login(self, username: str = None) -> requests.Response:
        if username is not None:
            self._payload.set_username(username)
        return self._session.get(self.login_url, timeout=self._timeout)

    def verify(self, captcha: str, err_id: str) -> tuple[dict[str, str], str | None]:
        self._payload.set_captcha(captcha)
        resp = self._session.post(self.login_url, self._payload.data)

        if (err := Erros.err(resp, err_id)) is not None:
            return ({}, err)

        return (self.fetch_data(resp), err)

    def fetch_captcha(self) -> bytes:
        return self._session.get(self.captcha_url, timeout=self._timeout).content

    def set_login_url(self, value: str | int) -> str:
        self._login_url = f"https://ptc.gov.ye/?page_id={value}"

    def set_captcha_url(self, value: str) -> None:
        self._captcha_url = f"https://ptc.gov.ye/wp-content/plugins/{value}/securimage/securimage_show.php?{str(random.random())}"

    def fetch_data(self, resp: requests.Response) -> dict[str, str]:
        pass

    @property
    def login_url(self) -> str:
        return self._login_url

    @property
    def captcha_url(self) -> str:
        return self._captcha_url
