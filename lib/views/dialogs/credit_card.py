
#!/usr/bin/python3
# -*- coding: utf-8 -*-

import flet as ft
import requests
from ...scrapper.adsl import ADSL
from ...constant import Dialogs
from ...models.user import User


class CreditCardDialog(ft.BottomSheet):
    def __init__(self, 
                 page: ft.Page,
                 user_id: int):
        super().__init__(ft.Control)

        self.isp = ADSL()
        self.isp.set_cookies(User.get_user(user_id).cookies)

        self.page = page

        self.enable_drag = True
        self.use_safe_area = True
        self.show_drag_handle = True
        self.is_scroll_controlled = True

        self.msg_label = ft.Ref[ft.Text]()
        
        self.content = ft.SafeArea(
            minimum_padding=15,
            content=ft.Column(                
                controls=[
                    ft.Column(
                        expand=True,
                        scroll=ft.ScrollMode.HIDDEN,
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            ft.TextField(
                                max_length=16,
                                label=f"الكرت رقم {index + 1}" + (" (اختياري) " if index > 0 else " (مطلوب) "),
                                keyboard_type=ft.KeyboardType.NUMBER,
                                input_filter=ft.NumbersOnlyInputFilter(),
                                on_focus=self.on_credit_field_focus
                            )
                            for index in range(15)
                        ]
                    ),
                    ft.Row(
                        alignment=ft.MainAxisAlignment.END,
                        controls=[
                            ft.ElevatedButton(
                                text = "الغاء", 
                                color = ft.colors.RED,
                                on_click=self.close
                            ),
                            ft.ElevatedButton(
                                text = "تجديد",
                                on_click=self.on_submit
                            )
                        ]
                    ),
                    ft.Text(
                        ref=self.msg_label,
                        color=ft.colors.RED,
                        size=14
                    )
                ]
            )
        )

    def on_credit_field_focus(self, e: ft.ControlEvent = None):
        fields = self.content.content.controls[0].controls
        fields[0].error_text = "الكرت الاول مطلوب" if e.control != fields[0] and not fields[0].value else None
        self.update()

    def close(self, e: ft.ControlEvent = None):
        self.page.close(self)

    def open_dialog(self):
        self.page.open(self)

    def on_submit(self, e: ft.ControlEvent):
        fields = self.content.content.controls[0].controls
        if not fields[0].value:
            return

        try:
            _, err = self.isp.fetch_credit([card.value for card in fields])
            if err is not None:
                self.msg_label.current.value = err
                self.msg_label.current.update()
            else:
                self.close()
        except requests.exceptions.ConnectionError:
            # No Internet Connection
            Dialogs.no_internet_connection(self.page)
        except Exception as err:
            # Unknow Error!
            Dialogs.error(err, self.page)