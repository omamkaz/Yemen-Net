#!/usr/bin/python3
# -*- coding: utf-8 -*-

import flet as ft
from ..models.user import User
from ..constant import ACCOUNT_TYPES
from .user_base import UserViewBase


class UserViewEdit(UserViewBase):
    def __init__(self, page: ft.Page, user_id: int):
        super().__init__(page, ft.icons.MODE_EDIT)

        self.user_id = user_id

        user = User.get_user(user_id)

        self.dname.value = user.dname
        self.username.value = user.username

        if user.atype == 0:
            self.password.value = user.password

        self.password.visible = user.atype == 0
        self.title.current.value = ACCOUNT_TYPES[user.atype]
        self.logo.current.src = f"/atype/{user.atype}.png"

        self.drop_down.current.value = user.atype

    def on_submit(self, e: ft.ControlEvent = None):
        super().on_submit(e)

        User.edit_user(
            self.user_id,
            int(self.drop_down.current.value),
            self.username.value, 
            self.password.value,
            self.dname.value
        )

        self.on_submit_done()