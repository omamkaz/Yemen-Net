#!/usr/bin/python3
# -*- coding: utf-8 -*-

import flet as ft
from ...constant import Refs
from ...models.user import User
from .list_tile import UserListTile


class UserListView(ft.ListView):
    def __init__(self, page: ft.Page, **kwargs):
        super().__init__(**kwargs)

        self.page = page
        self.spacing = 6
        self.expand = True
        self.controls = [
            self.new_item(i, user)
            for i, user in enumerate(User.get_users(), 1)
        ]

    def new_item(self, index: int, user) -> UserListTile:
        return UserListTile(
            page=self.page,
            index=index,
            atype=user.atype,
            title=user.dname or f"حساب رقم {index}",
            subtitle=user.username,
            verified=user.data is not None,
            data=user.id
        )

    def update_list(self):
        self.controls.clear()
        for i, user in enumerate(User.get_users(), 1):
            self.controls.append(
                self.new_item(i, user)
            )
        self.update()

    def set_selected_item(self, control: UserListTile | int) -> None:
        if isinstance(control, int):
            control = self.controls[control]

        for c in self.controls:
            c.selected = (c == control)

        self.update()

    def select_item(self, control: UserListTile | int) -> None:
        if isinstance(control, int):
            control = self.controls[control]

        self.page.client_storage.set("cur_user", control._index - 1)
        Refs.users.current.set_selected_item(control)
        Refs.cards.current.get_card(control._atype).set_data(control.data)
