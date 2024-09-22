#!/usr/bin/python3
# -*- coding: utf-8 -*-

import flet as ft

from .list_tile import CardTitle
from .credit import CardCredit
from .item import CardItem
from ...models.user import User
 

class Card(ft.GestureDetector):
    _user_id: int = None
    _isp = None

    def __init__(self, page: ft.Page, atype: int | str = 0, **kwargs):
        super().__init__(**kwargs)

        self.page = page

        self.card_title: CardTitle = CardTitle(atype)
        self.card_credit: CardCredit = CardCredit()
        self.card_items = ft.Ref[ft.Column]()

        self.on_pan_end = self._on_pan_end
        self.on_pan_update = self._on_pan_update

        self.content = ft.Container(
                expand=True,
                padding=0,
                margin=ft.margin.only(left=14, right=14, top=25),
                height=320,
                border_radius=14,
                alignment=ft.alignment.center,
                animate=ft.Animation(200, ft.AnimationCurve.LINEAR_TO_EASE_OUT),
                bgcolor=self.page.theme.color_scheme_seed + "800",
                shadow=ft.BoxShadow(
                    spread_radius=-10,
                    blur_radius=8,
                    color=ft.colors.with_opacity(ft.colors.BLACK, 0.07),
                    offset=ft.Offset(0, 8)
                ),
                content = ft.Column(
                    spacing=0,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        self.card_title,
                        self.card_credit,
                        ft.Column(
                            ref=self.card_items,
                            spacing=0,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER
                        )
                    ]
                )
            )

    def set_card_items(self, data: dict[str, str]) -> None:
        self.card_items.current.controls.clear()
        self.card_items.current.controls.extend(
            CardItem(label, value, end=(index == len(data) - 1))
            for index, (label, value) in enumerate(data.items())
        )

    def set_data(self, user_id: int, display: bool = False) -> None:
        self._user_id = user_id

        if self._user.data is not None:
            self.set_card_data()
        elif not display:
            self.login_web()

    def _on_pan_update(self, e: ft.DragUpdateEvent) -> None:
        if self.content.margin.top < (25 + 8) and e.delta_y >= 0:
            self.content.margin.top += min(0.8, e.delta_y) * 5 # 0.5
            self.content.update()

    def _on_pan_end(self, e: ft.DragEndEvent) -> None:
        if self.content.margin.top >= (25 + 8):
            if self._user_id is not None:
                self.login_web()
            elif len(User.get_users()) > 0:
                self.set_data(User.get_users()[0].id)

        self.content.margin.top = 25
        self.content.update()

    @property
    def _user(self):
        return User.get_user(self._user_id)