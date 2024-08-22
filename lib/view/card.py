#!/usr/bin/python3
# -*- coding: utf-8 -*-

import flet as ft
from .account_image import YAccountImage
from ..model.user_data import UserData


class YCard(ft.Container):
    def __init__(self):
        super().__init__()

        font_color = ft.colors.BLACK

        self.on_click = self.toggle_card_background_image

        self.bg_image = ft.Ref[ft.Image]()
        self.credit_calc = ft.Ref[ft.Text]()

        self.account_credit = ft.Text(
            text_align="center",
            size=20,
            color=font_color
        )
        self.account_image = YAccountImage()
        self.account_name = ft.Text(
            font_family="Cairo",
            color = font_color,
            expand=2
        )

        self.account_expir_date = ft.Text(
            size=13,
            color = font_color
        )

        self.account_status = ft.CircleAvatar(
            bgcolor=ft.colors.GREEN, 
            radius=6, 
            visible=False
        )

        self.account_type = ft.Text(
            size = 11, 
            text_align="center",
            color = font_color
        )

        self.margin = ft.margin.only(top=30)

        self.content = ft.Card(
            height=210,
            elevation=6,
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Container(
                        rtl=True,
                        margin=ft.margin.only(10, 10, 10),
                        content=ft.Row(
                            alignment=ft.MainAxisAlignment.START,
                            controls=[
                                ft.Stack(
                                    controls=[
                                        self.account_image,
                                        ft.Container(
                                            content = self.account_status,
                                            alignment=ft.alignment.bottom_right
                                        )
                                    ],
                                    width=40,
                                    height=40
                                ),
                                self.account_name,
                                ft.Container(
                                    content=ft.Image(
                                        ref = self.bg_image,
                                        src="assets/flag.png",
                                        width=32,
                                        height=32
                                    ),
                                    alignment=ft.alignment.top_left
                                )
                            ]
                        ),
                    ),
                    ft.Container(
                        margin=ft.margin.only(top=10),
                        content=ft.Column(
                            controls=[
                                ft.Text(
                                    value = "الرصيد", 
                                    text_align="center",
                                    size = 12,
                                    color = font_color
                                ),
                                ft.Row(
                                    controls=[
                                        self.account_credit,
                                        ft.Text(
                                            ref = self.credit_calc,
                                            visible=False,
                                            size=12,
                                            color = font_color
                                        )
                                    ],
                                    alignment=ft.MainAxisAlignment.CENTER
                                )
                            ],
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER
                        )
                    ),
                    self.account_type,
                    ft.Container(
                        margin=ft.margin.only(top=10),
                        content=self.account_expir_date,
                        alignment=ft.alignment.bottom_center
                    )
                ]
            )
        )

    def toggle_card_background_image(self, e: ft.ControlEvent):
        self.bg_image.current.visible = not self.bg_image.current.visible
        self.update()

    def set_credit_calc(self, prev_value: str, new_value: str):
        prev = float(prev_value.split()[0].strip())
        new = float(new_value.split()[0].strip())

        if prev == new:
            return

        if new > prev:
            value = new - prev
            prefix = "+"
            color = ft.colors.GREEN
        elif new < prev:
            value = prev - new
            prefix = "-"
            color = ft.colors.RED

        value = UserData.calc_credit(value)

        self.credit_calc.current.value = f"{prefix}{value}"
        self.credit_calc.current.color = color
        self.credit_calc.current.visible = True

    def set_data(self, 
                 atype: int | str,
                 username: str,
                 new_data: dict,
                 prev_data: dict = None):

        if prev_data is not None:
            self.set_credit_calc(
                prev_data.get("valid_credit"), 
                new_data.get("valid_credit")
            )
        else:
            self.credit_calc.current.visible = False

        self._atype = atype
        self._username = username

        user_data = UserData(new_data)

        self.account_name.value = user_data.name
        self.account_type.value = user_data.atype
        self.account_credit.value = user_data.credit
        self.account_expir_date.value = user_data.expir_date

        self.account_status.bgcolor = ft.colors.GREEN if user_data.status else ft.colors.RED
        self.account_status.visible = True

        self.account_image.set_image(int(atype))

        self.update()
    
    def clear_card(self):
        self._atype = None
        self._username = None

        self.account_name.value = ""
        self.account_credit.value = ""
        self.account_expir_date.value = ""
        self.account_type.value = ""

        self.account_status.visible = False
        self.credit_calc.current.visible = False

        self.update()