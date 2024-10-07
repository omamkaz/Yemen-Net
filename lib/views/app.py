#!/usr/bin/python3
# -*- coding: utf-8 -*-

import flet as ft

from ..views.cards import Cards
from ..views.list_user import UserListView
from ..views.bottom_bar import BottomAppBar
from ..constant import Refs, ThemeController


class Application:

    def on_close_window(self, e = None):
        size: list[int] = [self.page.window.width, self.page.window.height]
        self.page.client_storage.set("size", size)

    def set_current_user(self) -> None:
        cur_user_index: int = self.page.client_storage.get("cur_user") or 0
        if cur_user_index < 0 or not Refs.users.current.controls:
            Refs.cards.current.toggle_card(3)
            return

        Refs.users.current.select_item(cur_user_index)

    def __call__(self, page: ft.Page) -> None:
        self.page = page

        page.window.wait_until_ready_to_show = True
        page.horizontal_alignment = page.vertical_alignment = "center"

        page.title = "رصيد يمن نت"
        page.window.icon = "assets/icon.png"
        page.theme_mode = ThemeController.get_theme_mode(page)
        ThemeController.set_theme_color(ThemeController.get_theme_color(page), page)
        page.fonts = {
            "linaround": "/fonts/linaround_regular.otf"
        }

        page.padding = 0
        page.expand = True

        ft.SystemOverlayStyle.enforce_system_status_bar_contrast = True
        ft.SystemOverlayStyle.enforce_system_navigation_bar_contrast = True

        if page.platform not in (ft.PagePlatform.ANDROID, ft.PagePlatform.IOS):
            page.on_close = self.on_close_window

            page.window.min_width = 330
            page.window.min_height = 600

            page.window.max_width = 600
            page.window.max_height = 700
            
            if page.client_storage.contains_key("size"):
                page.window.width = page.client_storage.get("size")[0]
                page.window.height = page.client_storage.get("size")[1]

        page.bottom_appbar = BottomAppBar(page)
        page.floating_action_button_location = ft.FloatingActionButtonLocation.CENTER_DOCKED
        page.floating_action_button = ft.FloatingActionButton(
            mini=True,
            icon=ft.icons.ADD,
            on_click=lambda e: Cards.open_new_user_dialog(page)
        )

        page.add(
            ft.SafeArea(
                expand=True,
                content=ft.Column(
                    expand=True,
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Stack(
                            controls=[
                                ft.Container(
                                    padding=0,
                                    margin=0,
                                    height=250,
                                    border_radius=ft.BorderRadius(0, 0, 42, 42),
                                    bgcolor=page.theme.color_scheme_seed
                                ),
                                Cards(page, ref=Refs.cards)
                            ]
                        ),
                        UserListView(page, ref=Refs.users)
                    ]
                )
            )
        )

        self.set_current_user()