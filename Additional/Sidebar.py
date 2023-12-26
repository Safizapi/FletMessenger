from flet import Page, Container, margin, Row, Column, icons, Icon


class Sidebar:
    def __init__(self, page: Page):
        self.page = page

    def new_icon(self, icon: icons, navigation: str) -> Row:
        return Row(
            controls=[
                Column(
                    expand=True,
                    controls=[
                        Row(
                            controls=[Container(
                                expand=True,
                                height=60,
                                content=Icon(
                                    icon,
                                    color="#FFFFFF",
                                    size=30,
                                ),
                                on_click=lambda _: self.page.go(navigation)
                            )],
                            scroll=None
                        )
                    ]
                )
            ]
        )

    def sidebar(self) -> Container:
        chat_icon = self.new_icon(icons.CHAT_BUBBLE, "/chats")
        settings_icon = self.new_icon(icons.SETTINGS, "/settings")
        log_out_icon = self.new_icon(icons.LOGOUT, "/")

        bar = Container(
            width=50,
            height=700,
            bgcolor="#323232",
            content=Row(
                controls=[
                    Column(
                        expand=True,
                        controls=[
                            chat_icon,
                            settings_icon,
                            log_out_icon
                        ]
                    )
                ]
            ),
            border_radius=10
        )

        bar.margin = margin.only(bottom=50)

        return bar
