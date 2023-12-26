from flet import Page, View, Text, TextField, ElevatedButton, MainAxisAlignment, CrossAxisAlignment, UserControl
import sqlite3 as sql


class Login:
    def __init__(self, page: Page):
        self.page = page

    def login_page(self) -> None:
        def login(e: UserControl) -> None:
            conn = sql.connect("appDB.db")
            db = conn.cursor()

            info = list(db.execute("SELECT * FROM users WHERE username=?", (username.value,)))
            if info:
                if info[0][-1] == password.value:
                    self.page.go("/chats")

                    with open("username.txt", "w") as file:
                        file.write(username.value + "\n" + str(info[0][0]))
                else:
                    log_message.value = "Incorrect password"
                    self.page.update()
            else:
                log_message.value = "No account with that name"
                self.page.update()

        self.page.views.append(
            View(
                route="/",
                controls=[
                    Text(value="Authorization", size=30),
                    username := TextField(label="Username", width=300),
                    password := TextField(label="Password", password=True, can_reveal_password=True, width=300),
                    ElevatedButton(text="Login", on_click=login, width=100),
                    ElevatedButton(text="Register", on_click=lambda _: self.page.go("/register")),
                    log_message := Text()
                ],
                vertical_alignment=MainAxisAlignment.CENTER,
                horizontal_alignment=CrossAxisAlignment.CENTER,
                spacing=10
            )
        )
