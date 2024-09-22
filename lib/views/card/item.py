#!/usr/bin/python3
# -*- coding: utf-8 -*-

import flet as ft


class CardItem(ft.Container):
    def __init__(self, 
                 label: str = "", 
                 value: str = "",
                 end: bool = False,
                 **kwargs):
        super().__init__(**kwargs)

        self.margin=0
        self.padding = ft.padding.only(left=10, right=10)
        self.content = ft.Column(
            spacing=0,
            controls=[
                ft.Row(
                    spacing=0,
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        ft.Text(
                            value=value,
                            color=ft.colors.WHITE,
                            size=11,
                            text_align="left",
                            weight=ft.FontWeight.W_500,
                            overflow=ft.TextOverflow.CLIP,
                            font_family="circle_rounded",
                            selectable=True
                        ),
                        ft.Text(
                            value=label,
                            color=ft.colors.WHITE,
                            size=14,
                            font_family="linaround",
                            text_align="right"
                        )
                    ]
                )
            ]
        )

        if not end:
            self.content.controls.append(
                ft.Divider(
                    leading_indent=4,
                    trailing_indent=4
                )
            )
        else:
            self.margin = ft.margin.only(bottom=10)

    def hide_line(self) -> None:
        self.content.controls[-1].visible = False
        self.update()

    def show_line(self) -> None:
        self.content.controls[-1].visible = True
        self.update()

    def _set_item_value(self, index: int, value: str) -> None:
        c = self.content.controls[0].controls[index]
        c.value = value
        self.update()

    def set_label(self, label: str):
        self._set_item_value(1, label)

    def set_value(self, value: str):
        self._set_item_value(0, value)