#!/usr/bin/python3
# -*- coding: utf-8 -*-

import flet as ft
from ...constant import LottieFiles


class CardTitle(ft.ListTile):
    def __init__(self, atype: int | str = 0):
        super().__init__()

        self.content_padding = ft.padding.only(right=10)

        self.title = ft.Text(
            size=14.5,
            color=ft.colors.WHITE,
            text_align="right"
        )

        self.subtitle = ft.Text(
            text_align="right",
            color=ft.colors.WHITE70,
            size=14
        )

        self.trailing = ft.Stack(
            alignment=ft.alignment.bottom_right,
            controls=[
                ft.Image(
                    src=f"/atype/{atype}.png",
                    width=42,
                    height=42
                ),
                ft.Badge(
                    small_size=13,
                    bgcolor=ft.colors.GREEN
                )
            ]
        )

        self.leading = ft.Container(
            content=ft.Lottie(
                src_base64=LottieFiles.down_arrow
            )
        )

    def set_loading(self, on: bool) -> None:
        self.leading.content.src_base64 = LottieFiles.loading_carga if on else LottieFiles.down_arrow
        self.leading.update()

    def set_active(self, on: bool = True) -> None:
        self.trailing.controls[-1].bgcolor = "green" if on else "red"
        self.update()

    def set_logo(self, atype: int | str) -> None:
        self.trailing.controls[0].src = f"/atype/{atype}.png"
        self.update()

    def set_title(self, title: str) -> None:
        self.title.value = title
        self.update()

    def set_subtitle(self, subtitle: str) -> None:
        self.subtitle.value = subtitle
        self.update()

