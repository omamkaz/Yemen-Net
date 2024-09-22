#!/usr/bin/python3
# -*- coding: utf-8 -*-

import flet as ft
from typing import Callable, Sequence
from ..constant import THEME_COLORS, ThemeController


class ThemeButtonGroup(ft.Row):
    def __init__(self, 
                 colors: Sequence[str],
                 on_change: Callable):
        super().__init__()

        self.scroll = ft.ScrollMode.ADAPTIVE
        self.alignment = ft.MainAxisAlignment.CENTER

        self.on_change = on_change
        self.controls = [
            ft.Container(
                width=32,
                height=32,
                data=color,
                bgcolor=color,
                on_click = self._on_click,
                shape=ft.BoxShape.CIRCLE
            )
            for color in colors
        ]

    def _on_click(self, e: ft.ControlEvent) -> None:
        e.control.border = ft.border.all(3, e.control.bgcolor + "100")
        for c in self.controls:
            if e.control != c:
                c.border = None
        self.update()
        self.on_change(e.control.data)


class ThemeDialog(ft.BottomSheet):
    def __init__(self, page: ft.Page):
        super().__init__(ft.Control)
        
        self.page = page

        mode = (self.page.client_storage.get("theme_mode") 
                or self.page.platform_brightness.name).lower()

        self.enable_drag = True
        self.show_drag_handle = True

        self.content = ft.Container(
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
                            THEME_COLORS,
                            on_change=lambda color: ThemeController.set_theme_color(color, self.page)
                        )
                    )
                ]
            )
        )
