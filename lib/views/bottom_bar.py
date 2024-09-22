#!/usr/bin/python3
# -*- coding: utf-8 -*-

import flet as ft
from .about_dialog import AboutDialog
from .theme_dialog import ThemeDialog


class BottomAppBar(ft.BottomAppBar):
    def __init__(self, page: ft.Page):
        super().__init__()

        self.page = page

        self.height = 55
        self.notch_margin = 8
        self.shape = ft.NotchShape.CIRCULAR
        self.padding = ft.padding.only(left=10, right=10)
        self.content = ft.Row(
            controls=[
                ft.IconButton(
                    icon=ft.icons.INFO,
                    on_click=self.open_about_dialog
                ),
                ft.IconButton(
                    icon=ft.icons.COLORIZE,
                    on_click=self.open_theme_dialog
                )
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        )

    def open_about_dialog(self, e: ft.ControlEvent) -> None:
        about = AboutDialog(self.page)
        self.page.open(about)

    def open_theme_dialog(self, e: ft.ControlEvent) -> None:
        theme = ThemeDialog(self.page)
        self.page.open(theme)