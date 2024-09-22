#!/usr/bin/python3
# -*- coding: utf-8 -*-

import flet as ft
from humanize import naturalsize


USERNAME = "omamkaz"
ACCOUNT_TYPES = ("Yemen Net (ADSL)", "4G LTE", "Phone")
ABOUT_LINK_ICONS = (
    ("google", "#db4437", f"mailto:{USERNAME}@gmail.com"),
    ("paypal", "#00a7ce", f"PayPal.me/{USERNAME}"),
    ("telegram", "#0088cc", f"https://t.me/{USERNAME}"),
    ("whatsapp", "#25d366", "https://wa.me/967776973923"),
    ("github", "#000000", f"https://www.github.com/{USERNAME}"),
    ("twitter", "#1da1f2", f"https://www.twitter.com/{USERNAME}"),
    ("facebook", "#1877f2", f"https://www.facebook.com/{USERNAME}")
)
THEME_COLORS = (
    "INDIGO", "AMBER", "BLUE", 
    "BROWN", "CYAN", "GREEN", 
    "GREY", "LIME", "ORANGE", 
    "PINK", "PURPLE", "RED", 
    "TEAL", "YELLOW"
)

class UserData:

    @staticmethod
    def custom_credit(value: str | float | int) -> str:
        return naturalsize(float(value) * 10**9, format="%.2f")

    @classmethod
    def filter_data(cls, data: dict[str, str], atype: int | str) -> dict[str, str]:
        return getattr(cls, f"type_{atype}")(data)

    @classmethod
    def type_0(cls, data: dict[str, str]) -> dict[str, str]:
        for k, v in data.items():
            if isinstance(v, str) and "جيجابايت" in v:
                u, _ = v.strip().split()
                v = UserData.custom_credit(u.strip())
                data[k] = v
        return data

    @classmethod
    def type_1(cls, data: dict[str, str]) -> dict[str, str]:
        for k, v in data.items():
            if "gb" in k.lower():
                u, _ = v.split()
                v = UserData.custom_credit(u.strip())
                data[k] = v
        return data

    @classmethod
    def type_2(cls, data: dict[str, str]) -> dict[str, str]:
        return data



class Refs:
    cards = ft.Ref[ft.Container]()
    users = ft.Ref[ft.ListView]()


class ThemeController:

    @staticmethod
    def toggle_theme_mode(theme_mode: str, page: ft.Page) -> None:
        page.client_storage.set("theme_mode", theme_mode)
        page.theme_mode = theme_mode
        page.update()

    @staticmethod
    def set_theme_color(color: str, page: ft.Page) -> None:
        page.theme = page.dark_theme = ft.Theme(
            color_scheme_seed=color,
            use_material3=True,
            font_family="linaround",
            primary_color=color + "900",
            divider_theme=ft.DividerTheme(
                color = color + "900"
            )
        )

        if page.controls:
            controls = page.controls[0].content.controls[0].controls
            controls[0].bgcolor = color

            for c in controls[1].controls:
                c.content.bgcolor = color + "800"

        page.client_storage.set("theme_color", color)
        page.update()


class Dialogs:
    
    @staticmethod
    def no_internet_connection(page: ft.Page) -> None:
        page.open(
            ft.AlertDialog(
                icon=ft.Icon(ft.icons.WIFI_OFF, ft.colors.RED),
                content=ft.Text(
                    rtl=True,
                    value = "لايوجد اتصال انترنت!",
                    text_align="center"
                )
            )
        )
    
    @staticmethod
    def error(err: str, page: ft.Page) -> None:
        page.open(
            ft.AlertDialog(
                icon=ft.Icon(ft.icons.ERROR, ft.colors.RED),
                content=ft.Text(
                    value = str(err),
                    text_align="center"
                )
            )
        )
