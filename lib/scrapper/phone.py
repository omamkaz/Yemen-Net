#!/usr/bin/python3

import random
import requests
from .base import Base, ParserError


class Phone(Base):
    URL = Base.URL + "2354"

    def __init__(self):
        super().__init__()

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
            table = tuple(resp_soup.find("table", class_="transdetail").find_all("tr"))

            data = {}
            for tr in table[1:]:
                data[tr.find("th").text.strip().replace(":", "")] = tr.find("span").text.strip()

            return data
        except AttributeError:
            raise ParserError("لايمكنك الاستعلام في الوقت الحالي .لقد تجازوت عدد مرات الاستعلام المسموح بها ")

    @property
    def _captcha_url(self) -> str:
        return f"https://ptc.gov.ye/wp-content/plugins/quarybill-api-plug/securimage/securimage_show.php?{random.random()}"
