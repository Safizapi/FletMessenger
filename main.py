from flet import ViewPopEvent, Page, app
from flet import RouteChangeEvent, View
from views.Login import Login
from views.Register import Register
from views.Chats import Chats
from views.Settings import Settings


def main(page: Page) -> None:
    page.title = "Flet Messenger"
    page.window_height = 700
    page.window_width = 500
    
    def route_change(e: RouteChangeEvent) -> None:
        page.views.clear()

        # Login
        Login(page).login_page()

        # Registration
        Register(page).register_page()

        # Chats
        Chats(page).chats_page()

        # Settings
        Settings(page).settings_page()

        page.update()

    def view_pop(e: ViewPopEvent) -> None:
        page.views.pop()
        top_view: View = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)

    if open("username.txt").readline():
        page.go("/chats")


if __name__ == "__main__":
    app(target=main)
