
import flet as ft

from .models.user import User
from .views.user_new import UserViewNew
from .views.list_user import UserListView
from .views.bottom_bar import BottomAppBar
from .constant import Refs, ThemeController
from .views.cards import ADSLCard, LTECard, PhoneCard, Card


class Cards(ft.Stack):
    def __init__(self, page: ft.Page, **kwargs):
        super().__init__(**kwargs)
        self.page = page

        self.controls = [
            ADSLCard(page),
            LTECard(page, visible=False),
            PhoneCard(page, visible=False),
            ft.Lottie(
                src="/lottie/online-health-report.json"
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
        self.page.client_storage.set("size", [self.page.window.width, self.page.window.height])

    def __call__(self, page: ft.Page) -> None:
        self.page = page

        page.window.wait_until_ready_to_show = True

        page.title = "الاستعلام عن رصيد يمن نت"
        page.window.icon = "icon.png"
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
            "linaround": "fonts/linaround_regular.otf"
        }

        ThemeController.set_theme_color(page.client_storage.get("theme_color") or "INDIGO", page)

        page.bottom_appbar = BottomAppBar(page)
        page.floating_action_button_location = ft.FloatingActionButtonLocation.CENTER_DOCKED
        page.floating_action_button = ft.FloatingActionButton(
            icon=ft.icons.ADD,
            mini=True,
            on_click=self.open_user_view_new
        )

        # ft.SystemOverlayStyle.enforce_system_status_bar_contrast = True
        # ft.SystemOverlayStyle.enforce_system_navigation_bar_contrast = True

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
                                Cards(page, ref=Refs.cards),
                            ]
                        ),
                        UserListView(ref=Refs.users)
                    ]
                )
            )
        )

        if (users := User.get_users()) and (user := users[0]).data is not None:
            card = Refs.cards.current.toggle_card(user.atype)
            card.set_data(user.id, True)
        else:
            Refs.cards.current.toggle_card(3)


if __name__ == "__main__":
    ft.app(target=Application())