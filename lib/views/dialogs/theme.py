#!/usr/bin/python3
# -*- coding: utf-8 -*-

import flet as ft
from typing import Callable, Sequence
from ...constant import THEME_COLORS, ThemeController


class ThemeButtonGroup(ft.Row):
    def __init__(self,
                 value: str,
                 colors: Sequence[str],
                 on_change: Callable):
        super().__init__()

        self.scroll = ft.ScrollMode.HIDDEN
        self.alignment = ft.MainAxisAlignment.CENTER

        self.on_change = on_change
        self.controls = [
            ft.Container(
                key=color,
                width=32,
                height=32,
                bgcolor=color,
                on_click=self._on_click,
                shape=ft.BoxShape.CIRCLE,
                border=None if color != value else ft.border.all(3, value + "100")
            )
            for color in colors
        ]

    def select_color(self, color: str) -> None:
        for i, c in enumerate(self.controls):
            if i <= len(self.controls) - 1:
                c.border = None if c.key != color else ft.border.all(3, c.bgcolor + "100")
            else:
                c.border = ft.border.all(3, ft.colors.BLACK12)

        self.update()

    def _on_click(self, e: ft.ControlEvent) -> None:
        self.select_color(e.control.key)
        self.on_change(e.control.key)


class ThemeDialog(ft.BottomSheet):
    def __init__(self, page: ft.Page):
        super().__init__(ft.Control)
        
        self.page = page

        mode = (self.page.client_storage.get("theme_mode") 
                or self.page.platform_brightness.name).lower()

        self.enable_drag = True
        self.show_drag_handle = True

        self.content = ft.SafeArea(
            expand=True,
            minimum_padding=ft.padding.only(left=5, right=5),
            content=ft.Column(
                alignment=ft.MainAxisAlignment.SPACE_AROUND,
                controls=[
                    ft.RadioGroup(
                        value=mode,
                        content=ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_AROUND,
                            vertical_alignment=ft.CrossAxisAlignment.END,
                            controls=[
                                ft.Column(
                                    alignment=ft.MainAxisAlignment.CENTER,
                                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                    controls=[
                                        ft.Icon(
                                            name=icon,
                                            size=64
                                        ),
                                        ft.Radio(
                                            value=name,
                                            tooltip=tooltip
                                        )
                                    ]
                                )
                                for icon, name, tooltip in zip(
                                    [ft.icons.BRIGHTNESS_MEDIUM, ft.icons.DARK_MODE, ft.icons.LIGHT_MODE], 
                                    ["system", "dark", "light"], 
                                    ["اتبع نمط النظام", "الوضع الليلي", "الوضع النهاري"]
                                )
                            ]
                        ),
                        on_change=lambda e: ThemeController.toggle_theme_mode(e.data, self.page)
                    ),
                    ft.Container(
                        margin=ft.margin.only(left=25, right=25),
                        content=ThemeButtonGroup(
                            value=page.client_storage.get("theme_color") or THEME_COLORS[0],
                            colors=THEME_COLORS,
                            on_change=lambda color: ThemeController.set_theme_color(color, self.page)
                        )
                    )
                ]
            )
        )
