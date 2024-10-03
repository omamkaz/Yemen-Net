#!/usr/bin/python3
# -*- coding: utf-8 -*-

import flet as ft
from .card import Card
from .dialogs import NewUserDialog
from ..constant import LottieFiles
from .atypes import ADSLCard, LTECard, PhoneCard


class Cards(ft.Stack):
    def __init__(self, page: ft.Page, **kwargs):
        super().__init__(**kwargs)
        self.page = page

        self.controls = [
            ADSLCard(page, visible=False),
            LTECard(page, visible=False),
            PhoneCard(page, visible=False),
            ft.Container(
                ft.Lottie(
                    fit=ft.ImageFit.COVER,
                    src_base64=LottieFiles.online_health_report
                ),
                on_click=lambda e: self.open_new_user_dialog(self.page)
            )
        ]

    def toggle_card(self, atype: int | str = 3) -> Card:
        for i, c in enumerate(self.controls):
            c.visible = (i == int(atype))
        self.update()
        return self.controls[int(atype)]

    @classmethod
    def open_new_user_dialog(cls, page: ft.Page) -> None:
        user_view_new = NewUserDialog(page)
        page.open(user_view_new)
