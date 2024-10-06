#!/usr/bin/python3
# -*- coding: utf-8 -*-

import flet as ft
from .card import Card
from .dialogs import NewUserDialog
from ..constant import LottieFiles, Refs
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
                content=ft.Lottie(
                    fit=ft.ImageFit.COVER,
                    src_base64=LottieFiles.online_health_report
                ),
                alignment=ft.alignment.center,
                on_click=lambda e: self.open_new_user_dialog(self.page)
            ),
            ft.Container(
                content=ft.Lottie(
                    fit=ft.ImageFit.COVER,
                    src_base64=LottieFiles.pin_required
                ),
                alignment=ft.alignment.center,
                on_click=self.on_verify_click
            )
        ]

    def toggle_card(self, atype: int | str = 3) -> Card:
        for i, c in enumerate(self.controls):
            c.visible = (i == int(atype))
        self.update()
        return self.controls[int(atype)]

    def get_card(self, atype: int | str) -> Card:
        return self.controls[int(atype)]

    @classmethod
    def open_new_user_dialog(cls, page: ft.Page) -> None:
        user_view_new = NewUserDialog(page)
        page.open(user_view_new)

    def on_verify_click(self, e: ft.ControlEvent) -> None:
        cur_user_index: int = self.page.client_storage.get("cur_user") or 0
        control: int = Refs.users.current.controls[cur_user_index]
        self.get_card(control._atype).set_login(control.data)