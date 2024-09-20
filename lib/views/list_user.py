#!/usr/bin/python3
# -*- coding: utf-8 -*-

import flet as ft
from typing import Callable
from ..constant import Refs
from .user_edit import UserViewEdit
from ..viewmodels.user_vm import UserViewModel


class ListTile(ft.ListTile):
    def __init__(self,
                 atype: int,
                 title: str, 
                 subtitle: str,
                 **kwargs):
        super().__init__(**kwargs)

        self.vm = UserViewModel()

        self.on_click = self._on_click
        self.on_long_press = self.toggle_action_buttons

        self.title = ft.Text(value = title, rtl=True)
        self.subtitle = ft.Text(value = subtitle, rtl=True)
        self.trailing = ft.Image(
            src = f"assets/atype/{atype}.png",
            width=38,
            height=38
        )
        self.leading = ft.Row(
            controls=[
                ft.IconButton(
                    icon=ft.icons.DELETE,
                    icon_color=ft.colors.RED_500,
                    on_click=self.on_delete
                ),
                ft.IconButton(
                    icon=ft.icons.EDIT,
                    on_click=self.on_edit
                )
            ],
            alignment=ft.MainAxisAlignment.START,
            width=70,
            spacing=0,
            visible=False
        )
    
    def _set_list_state(self, on: Callable) -> None:
        for c in Refs.user_list.current.controls:
            c.leading.visible = on(c)
        Refs.user_list.current.update()

    def _on_click(self, e: ft.ControlEvent) -> None:
        self._set_list_state(lambda _: False)
        Refs.card.current.set_data(self.data)

    def toggle_action_buttons(self, e: ft.ControlEvent) -> None:
        self._set_list_state(lambda x: x == self)

    def on_delete(self, e: ft.ControlEvent) -> None:
        self.vm.delete_user(self.data)
        Refs.user_list.current.update_list()

        if Refs.user_list.current.controls:
            Refs.card.current.set_data(Refs.user_list.current.controls[0].data)

    def on_edit(self, e: ft.ControlEvent):
        user_view_edit = UserViewEdit(self.page, self.data)
        self.page.open(user_view_edit)


class UserListView(ft.ListView):
    def __init__(self):
        super().__init__(ref=Refs.user_list)

        self.vm = UserViewModel()

        self.spacing = 6
        self.expand = True
        self.padding = ft.padding.only(6, 6, 0, 6)
        self.controls = [
            self.new_item(i, user)
            for i, user in enumerate(self.vm.get_users(), 1)
        ]

    def new_item(self, index: int, user) -> ListTile:
        return ListTile(
            user.atype,
            user.dname or f"حساب رقم {index}",
            user.username,
            data=user.id
        )

    def update_list(self):
        self.controls.clear()
        for i, user in enumerate(self.vm.get_users(), 1):
            self.controls.append(self.new_item(i, user))
        self.controls.sort(key=lambda c: c.title.value)
        self.update()
