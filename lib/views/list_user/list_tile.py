#!/usr/bin/python3
# -*- coding: utf-8 -*-

import flet as ft
from ...constant import Refs
from ...models.user import User
from ..dialogs import EditUserDialog


class UserListTile(ft.ListTile):
    def __init__(self,
                 page: ft.Page,
                 index: int,
                 atype: int,
                 title: str,
                 subtitle: str,
                 verified: bool = False,
                 **kwargs):
        super().__init__(**kwargs)

        self._index = index
        self._atype = atype

        self.page = page

        self.on_click = self._on_click

        self.title = ft.Text(value = title, rtl=True)
        self.subtitle = ft.Text(value = subtitle, rtl=True)

        self.trailing = ft.Stack(
            alignment=ft.alignment.bottom_right,
            controls=[
                ft.Image(
                    src=f"/atype/{atype}.png",
                    width=38,
                    height=38
                ),
                ft.Image(
                    src="/verified.svg",
                    width=14,
                    height=14,
                    visible=verified
                )
            ]
        )

        self.leading = ft.PopupMenuButton(
            # menu_position=ft.PopupMenuPosition.OVER,
            tooltip="خيارات اخرى",
            items=[
                ft.PopupMenuItem(
                    text="تعديل",
                    icon=ft.icons.EDIT,
                    on_click=self.on_edit
                ),
                ft.PopupMenuItem(
                    text="حذف",
                    icon=ft.icons.DELETE,
                    on_click=self.on_delete
                )
            ]
        )

        self.selected_tile_color = ft.colors.with_opacity(0.09, self.page.theme.color_scheme_seed)

    def _on_click(self, e: ft.ControlEvent) -> None:
        Refs.users.current.select_item(self)

    def on_delete(self, e: ft.ControlEvent) -> None:
        def on_ok():
            self.page.close(alert)
            self.page.client_storage.set("cur_user", 0)

            User.delete_user(self.data)
            Refs.users.current.update_list()

            if Refs.users.current.controls:
                Refs.users.current.select_item(0)
            else:
                Refs.cards.current.toggle_card(3)

        alert = ft.AlertDialog(
            modal=True,
            title=ft.Text(
                value = f"هل أنت متأكد من انك تريد حذف {self.title.value}",
                rtl=True
            ),
            actions=[
                ft.ElevatedButton(
                    text="نعم",
                    on_click=lambda e: on_ok()
                ),
                ft.ElevatedButton(
                    text="لا",
                    autofocus=True,
                    on_click=lambda e: self.page.close(alert)
                )
            ]
        )
        self.page.open(alert)

    def on_edit(self, e: ft.ControlEvent):
        user_view_edit = EditUserDialog(self.page, self.data)
        self.page.open(user_view_edit)
