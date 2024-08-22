#!/usr/bin/python3
# -*- coding: utf-8 -*-

import typing
import humanize
import flet as ft

from datetime import datetime
from ..model.client_storage import ClientStorage
from ..view.account_image import YAccountImage


class YListItem(ft.ListTile):
    def __init__(self, 
                 atype: int | str,
                 username: str,
                 client_storage: ClientStorage,
                 on_click: typing.Callable = None,
                 on_long_press: typing.Callable = None,
                 on_delete_press: typing.Callable = None):
        super().__init__()

        self.data = (atype, username)
        self.client_storage = client_storage

        name = self.client_storage.get_user_data_key(atype, username, "name")

        self.rtl = True

        self.title = ft.Text(name or username, no_wrap=True)
        self.subtitle = ft.Text(username, no_wrap=True) if name else None

        self.leading = ft.Image(
            src=f"assets/{YAccountImage._images[int(atype)]}.png",
            width=32, 
            height=32
        )
        self.trailing = ft.IconButton(
            icon = ft.icons.DELETE, 
            icon_color = ft.colors.RED,
            on_click = on_delete_press,
            data = self.data,
            visible=False
        )

        self.on_click = on_click
        self.on_long_press = on_long_press