#!/usr/bin/python3
# -*- coding: utf-8 -*-

import flet as ft
from ..constant import ABOUT_LINK_ICONS


class LinkIcon(ft.IconButton):
    def __init__(self, 
                 icon: str,
                 color: str,
                 link: str,
                 page: ft.Page):
        super().__init__()

        self.page = page
        self.link = link
        self.tooltip = icon.title()
        self.on_click = self.on_open_url
        self.content = ft.Image(
            src = f"/logo/{icon}.svg",
            color=color,
            width=18,
            height=18
        )

    def on_open_url(self, e: ft.ControlEvent) -> None:
        if self.page.can_launch_url(self.link):
            self.page.launch_url(self.link)


class Link(ft.TextField):
    def __init__(self, 
                 label: str,
                 value: str):
        super().__init__(
            value=value,
            read_only=True,
            label=label,
            height=50,
            border_radius=5,
            cursor_height=16,
            content_padding=10,
            border_width=1.5,
            text_size=14
        )


class AboutDialog(ft.BottomSheet):
    def __init__(self, page: ft.Page):
        super().__init__(ft.Control)

        self.page = page

        self.enable_drag = True
        self.show_drag_handle = True

        self.content = ft.Column(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            horizontal_alignment="center",
            controls=[
                ft.Text(
                    value="عن المطور"
                ),
                ft.Container(
                    width=64,
                    height=64,
                    shape=ft.BoxShape("circle"),
                    image = ft.DecorationImage(
                        src="assets/me.jpg",
                        fit="cover"
                    )
                ),
                ft.Text("Osama Mohammed Al-zabidi", size=14),
                ft.Text(
                    "Software Developer | Python Programming | GUI & Web Apps",
                    weight="w400",
                    text_align="center",
                    size=10
                ),
                ft.Container(
                    margin=ft.margin.only(10, 20, 10),
                    content=ft.Column(
                        spacing=16,
                        controls=[
                            Link("Username", "@omamkaz"),
                            ft.Row(
                                spacing=0,
                                alignment=ft.MainAxisAlignment.CENTER,
                                controls=[
                                    LinkIcon(icon, color, link, page)
                                    for icon, color, link in ABOUT_LINK_ICONS
                                ]
                            )
                        ]
                    )
                ),

                ft.Container(
                    alignment=ft.alignment.center,
                    margin=ft.margin.only(right=10, bottom=10),
                    content=ft.Text(
                        value="v4.0.0",
                        weight=ft.FontWeight.BOLD,
                        font_family="Monospace",
                        text_align="center",
                        size=13
                    )
                )
            ]
        )