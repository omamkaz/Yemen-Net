#!/usr/bin/python3
# -*- coding: utf-8 -*-

import flet as ft

from .list_tile import CardTitle
from .credit import CardCredit
from .item import CardItem
from ...models.user import User
from ...constant import ThemeController, LottieFiles, Refs
 

class Card(ft.GestureDetector):
    _user_id: int = None
    _isp = None

    def __init__(self, page: ft.Page, atype: int | str = 0, **kwargs):
        super().__init__(**kwargs)

        self.page = page

        self.card_title: CardTitle = CardTitle(atype)
        self.card_credit: CardCredit = CardCredit()
        self.card_items = ft.Ref[ft.Column]()

        self.on_tap = self._on_tap
        self.on_pan_end = self._on_pan_end
        self.on_pan_update = self._on_pan_update

        self._image = ft.DecorationImage(
            src="assets/7oct.jpg",
            fit=ft.ImageFit.COVER,
            opacity=0.1
        )

        self.content = ft.Container(
                expand=True,
                padding=0,
                border_radius=16,
                height=self.card_height,
                alignment=ft.alignment.center,
                margin=ft.margin.only(left=14, right=14, top=25),
                animate=ft.Animation(200, ft.AnimationCurve.LINEAR_TO_EASE_OUT),
                bgcolor=ThemeController.get_color(self.page.theme.color_scheme_seed, 800),
                image=self._image,
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
        if len(data) >= 6:
            self.content.height = self.card_height + (20 * (len(data) - 5))
        else:
            self.content.height = self.card_height

    def set_data(self, user_id: int) -> None:
        self._user_id = user_id

        self.set_loading(True)
        if self._user.data is not None:
            Refs.cards.current.toggle_card(self._user.atype)
            self.set_card_data()
        else:
            Refs.cards.current.toggle_card(4)
        self.set_loading(False)

    def set_login(self, user_id: int) -> None:
        self._user_id = user_id

        self.set_loading(True)
        self.login_web()
        self.set_loading(False)

    def on_captcha_verify_submit(
            self,
            atype: int,
            data: dict[str, str],
            old_data: dict[str, str] = None,
            cookies: dict[str, str] = None) -> None:
        User.edit_data_and_cookies(self._user_id, data, cookies)
        self.set_card_data(old_data)
        Refs.cards.current.toggle_card(atype)
        for c in Refs.users.current.controls:
            c.selected = (self._user_id == c.data)
        Refs.users.current.update()

    def _on_pan_update(self, e: ft.DragUpdateEvent) -> None:
        if self.content.margin.top < (25 + 8) and e.delta_y >= 0:
            self.content.margin.top += min(0.8, e.delta_y) * 5
            self.content.update()

    def _on_pan_end(self, e: ft.DragEndEvent) -> None:
        if (self.content.margin.top >= (25 + 8) 
            and not self.is_loading() 
            and self._user_id is not None):

            self.set_loading(True)
            self.login_web()
            self.set_loading(False)

        self.content.margin.top = 25
        self.content.update()

    def _on_tap(self, e: ft.TapEvent) -> None:
        self.content.image = None if self.content.image is not None else self._image
        self.update()

    def set_loading(self, on: bool) -> None:
        self.page.views[0].disabled = on
        self.card_title.leading.content.src_base64 = LottieFiles.loading_carga if on else LottieFiles.down_arrow

        self.card_title.leading.update()
        self.page.update()

    def is_loading(self) -> bool:
        return self.page.views[0].disabled

    @property
    def card_height(self) -> int:
        return 320

    @property
    def _user(self) -> User:
        return User.get_user(self._user_id)