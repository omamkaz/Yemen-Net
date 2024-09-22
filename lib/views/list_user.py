#!/usr/bin/python3
# -*- coding: utf-8 -*-

import flet as ft
from typing import Callable
from ..constant import Refs
from ..models.user import User
from .user_edit import UserViewEdit


class ListTile(ft.ListTile):
    def __init__(self,
                 atype: int,
                 title: str, 
                 subtitle: str,
                 **kwargs):
        super().__init__(**kwargs)

        self.on_click = self._on_click
        self.on_long_press = self.toggle_action_buttons

        self.title = ft.Text(value = title, rtl=True)
        self.subtitle = ft.Text(value = subtitle, rtl=True)
        self.trailing = ft.Image(
            src = f"/atype/{atype}.png",
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
        for c in Refs.users.current.controls:
            c.leading.visible = on(c)
        Refs.users.current.update()

    def _on_click(self, e: ft.ControlEvent) -> None:
        self._set_list_state(lambda _: False)

        card = Refs.cards.current.toggle_card(User.get_user(self.data).atype)
        card.set_data(self.data)

    def toggle_action_buttons(self, e: ft.ControlEvent) -> None:
        self._set_list_state(lambda x: x == self)

    def on_delete(self, e: ft.ControlEvent) -> None:
        User.delete_user(self.data)
        Refs.users.current.update_list()

        if (users := Refs.users.current.controls):
            card = Refs.cards.current.toggle_card(User.get_user(users[0].data).atype)
            card.set_data(users[0].data)
        else:
            Refs.cards.current.toggle_card(3)

    def on_edit(self, e: ft.ControlEvent):
        user_view_edit = UserViewEdit(self.page, self.data)
        self.page.open(user_view_edit)


class UserListView(ft.ListView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.spacing = 6
        self.expand = True
        self.padding = ft.padding.only(6, 6, 0, 6)
        self.controls = [
            self.new_item(i, user)
            for i, user in enumerate(User.get_users(), 1)
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
        for i, user in enumerate(User.get_users(), 1):
            self.controls.append(self.new_item(i, user))
        self.controls.sort(key=lambda c: c.title.value)
        self.update()
