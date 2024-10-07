#!/usr/bin/python3

import requests
from .base import Base, ParserError


class Phone(Base):
    def __init__(self):
        super().__init__()

        self.set_login_url("2354")
        self.set_captcha_url("quarybill-api-plug")

        self._payload.username = "phoneid"
        self._payload.captcha = "captcha_code_qbill"

        self._payload.set("querybill_field", "78bc08868d")
        self._payload.set("_wp_http_referer", "/?page_id=2354")
        self._payload.set("doqbill", "querybillvalue")
        self._payload.set("qsubmit", "استعلام")

    def verify(self, captcha: str) -> tuple[dict[str, str], str | None]:
        return super().verify(captcha, "phoneidrror")

    def login(self, username: str) -> None:
        resp = super().login(username)
        soup = self.bs4(resp)

        value = soup.find("input", id="querybill_field").attrs.get("value")
        self._payload.set("querybill_field", value)

    def fetch_data(self, resp: requests.Response) -> dict:
        super().fetch_data(resp)

        try:
            resp_soup = self.bs4(resp)

            return {
                tr.find("th").text.strip().replace(":", ""): tr.find("span").text.strip()
                for tr in tuple(resp_soup.find("table", class_="transdetail").find_all("tr"))[1:]
            }
        except AttributeError:
            raise ParserError("لايمكنك الاستعلام في الوقت الحالي .لقد تجازوت عدد مرات الاستعلام المسموح بها ")