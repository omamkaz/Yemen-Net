
import flet as ft

from .models.user import User
from .views.user_new import UserViewNew
from .views.list_user import UserListView
from .views.bottom_bar import BottomAppBar
from .constant import Refs, ThemeController, LottieFiles
from .views.cards import ADSLCard, LTECard, PhoneCard, Card


class Cards(ft.Stack):
    def __init__(self, page: ft.Page, **kwargs):
        super().__init__(**kwargs)
        self.page = page

        self.controls = [
            ADSLCard(page),
            LTECard(page, visible=False),
            PhoneCard(page, visible=False),
            ft.Container(
                ft.Lottie(
                    fit=ft.ImageFit.COVER,
                    src_base64=LottieFiles.online_health_report
                ),
                on_click=lambda e: Application.open_user_view_new(self, e)
            )
        ]

    def toggle_card(self, atype: int | str = 3) -> Card:
        for i, c in enumerate(self.controls):
            c.visible = (i == int(atype))
        self.update()
        return self.controls[int(atype)]


class Application:

    def open_user_view_new(self, e: ft.ControlEvent):
        user_view_new = UserViewNew(self.page)
        self.page.open(user_view_new)

    def on_close_window(self, e = None):
        size: list[int] = [self.page.window.width, self.page.window.height]
        self.page.client_storage.set("size", size)

    def set_current_user(self) -> None:
        cur_user_index: int = self.page.client_storage.get("cur_user") or 0
        if (users := User.get_users()) and (user := users[cur_user_index]).data is not None:
            Refs.users.current.controls[cur_user_index].selected = True
            card = Refs.cards.current.toggle_card(user.atype)
            card.set_data(user.id, True)
            Refs.users.current.update()
        else:
            Refs.cards.current.toggle_card(3)

    def __call__(self, page: ft.Page) -> None:
        self.page = page

        page.window.wait_until_ready_to_show = True

        page.title = "رصيد يمن نت"
        page.window.icon = "assets/icon.png"
        page.theme_mode = page.client_storage.get("theme_mode") or page.platform_brightness.name.lower()

        page.padding = 0
        page.expand = True

        if page.platform not in (ft.PagePlatform.ANDROID, ft.PagePlatform.IOS):
            page.on_close = self.on_close_window

            page.window.min_width = 330
            page.window.min_height = 600

            page.window.max_width = 600
            page.window.max_height = 700
            
            if page.client_storage.contains_key("size"):
                page.window.width = page.client_storage.get("size")[0]
                page.window.height = page.client_storage.get("size")[1]

        page.horizontal_alignment = page.vertical_alignment = "center"
        page.fonts = {
            "linaround": "/fonts/linaround_regular.otf"
        }

        ThemeController.set_theme_color(page.client_storage.get("theme_color") or "INDIGO", page)

        page.bottom_appbar = BottomAppBar(page)
        page.floating_action_button_location = ft.FloatingActionButtonLocation.CENTER_DOCKED
        page.floating_action_button = ft.FloatingActionButton(
            mini=True,
            icon=ft.icons.ADD,
            on_click=self.open_user_view_new
        )

        ft.SystemOverlayStyle.enforce_system_status_bar_contrast = True
        ft.SystemOverlayStyle.enforce_system_navigation_bar_contrast = True

        page.add(
            ft.SafeArea(
                expand=True,
                content=ft.Column(
                    expand=True,
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Stack(
                            controls=[
                                ft.Container(
                                    padding=0,
                                    margin=0,
                                    height=250,
                                    border_radius=ft.BorderRadius(0, 0, 42, 42),
                                    bgcolor=page.theme.color_scheme_seed
                                ),
                                Cards(page, ref=Refs.cards)
                            ]
                        ),
                        UserListView(page, ref=Refs.users)
                    ]
                )
            )
        )

        self.set_current_user()
