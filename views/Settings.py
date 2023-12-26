from flet import Page, View, Text, CrossAxisAlignment, Row, TextField, ElevatedButton, Container, Column, UserControl
from Additional.Sidebar import Sidebar
import sqlite3 as sql


class Settings:
    def __init__(self, page: Page):
        self.page = page

    def settings_page(self) -> None:
        def change_nickname(e: UserControl):
            conn = sql.connect("appDB.db")
            db = conn.cursor()

            user_id = open("username.txt").readlines()[-1]

            check = list(db.execute("SELECT username=? FROM users", (username.value,)))

            if set(check) == {(0,)}:
                db.execute("UPDATE users SET username=? WHERE id=?", (username.value, user_id))
                conn.commit()

                name_log.value = f"Successfully changed username to {username.value}"
                self.page.update()
            else:
                name_log.value = "This username is already taken!"
                self.page.update()

        def change_password(e: UserControl) -> None:
            conn = sql.connect("appDB.db")
            db = conn.cursor()

            user_id = open("username.txt").readlines()[-1]

            db.execute("UPDATE users SET password=? WHERE id=?", (password.value, user_id))
            conn.commit()

            pass_log.value = f"Successfully changed password"
            self.page.update()

        if self.page.route == "/settings":
            screen = Container(
                expand=True,
                content=Column([Text("Changing username"), Row([
                    username := TextField(label="New username"),
                    ElevatedButton(text="Submit", on_click=change_nickname),
                    name_log := Text("")
                ]), Text("Changing password"), Row([
                    password := TextField(label="New password"),
                    ElevatedButton(text="Submit", on_click=change_password),
                    pass_log := Text("")
                ])])
            )

            self.page.views.append(
                View(
                    route="/settings",
                    controls=[
                        Text(value="User settings", size=20),
                        Container(
                            expand=True,
                            content=Row(
                                [
                                    Sidebar(self.page).sidebar(),
                                    screen
                                ],
                                spacing=700
                            )
                        )
                    ],
                    horizontal_alignment=CrossAxisAlignment.CENTER,
                    spacing=26
                )
            )
