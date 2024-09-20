#!/usr/bin/python3
# -*- coding: utf-8 -*-

import base64
import flet as ft
from typing import Callable
from ..scrapper.base import ParserError


class CaptchaVerify(ft.BottomSheet):
    def __init__(self, 
                 page: ft.Page, 
                 isp, 
                 callback: Callable, 
                 captcha_len: int = 4):
        super().__init__(ft.Control)

        self.page = page

        self.isp = isp
        self.callback = callback

        self.enable_drag = True
        self.show_drag_handle = True

        self.captcha_image = ft.Image(fit=ft.ImageFit.COVER)
        self.captcha_value = ft.TextField(
            input_filter=ft.InputFilter(r"^[0-9]*$"),
            text_align="center",
            max_length=captcha_len,
            autofocus=True,
            suffix=ft.IconButton(
                icon=ft.icons.REFRESH,
                on_click=self.on_refresh
            )
        )

        self.err_msg = ft.Text(
            size=13,
            rtl=True,
            color=ft.colors.RED
        )

        self.content = ft.Container(
            padding=ft.padding.only(left=15, right=15),
            content=ft.Column(
                controls=[
                    self.captcha_image,
                    self.captcha_value,
                    self.err_msg,
                    ft.Row(
                        alignment=ft.MainAxisAlignment.END,
                        controls=[
                            ft.ElevatedButton(
                                text = "الغاء", 
                                color = ft.colors.RED,
                                on_click=self.close
                            ),
                            ft.ElevatedButton(
                                text = "حفظ",
                                on_click=self.on_submit
                            )
                        ]
                    )
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            )
        )

    def close(self, e: ft.ControlEvent = None):
        self.page.close(self)

    def set_captcha_image(self, captcha: bytes):
        self.captcha_image.src_base64 = base64.b64encode(captcha).decode()

    def open_dialog(self):
        self.set_captcha_image(self.isp.fetch_captcha())
        self.page.open(self)

    def on_refresh(self, e: ft.ControlEvent):
        self.set_captcha_image(self.isp.fetch_captcha())
        self.update()

    def on_submit(self, e: ft.ControlEvent):
        try:
            data, err = self.isp.verify(self.captcha_value.value)

            if err is not None:
                self.err_msg.value = err
                self.err_msg.visible = True
            else:
                self.err_msg.visible = False
                self.close()
                self.callback(data)

            self.err_msg.update()
        except ParserError as err:
            self.page.open(
                ft.AlertDialog(
                    icon=ft.Icon(ft.icons.ERROR, ft.colors.RED),
                    content=ft.Text(
                        value = str(err),
                        text_align="center"
                    )
                )
            )