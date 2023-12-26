from flet import Page, View, Text, TextField, ElevatedButton, MainAxisAlignment, CrossAxisAlignment, AppBar, UserControl
import sqlite3 as sql


class Register:
    def __init__(self, page: Page):
        self.page = page

    def register_page(self) -> None:
        def register(e: UserControl):
            conn = sql.connect("appDB.db")
            db = conn.cursor()

            check = list(db.execute("SELECT username=? FROM users", (username.value,)))

            if set(check) == {(0,)} or not check:
                db.execute("INSERT INTO users VALUES (NULL, ?, ?)", (username.value, password.value))
                conn.commit()

                log_message.value = f"Successfully registered {username.value}"
                self.page.update()
            else:
                log_message.value = "Account with this name already exists!"
                self.page.update()

        if self.page.route == "/register":
            self.page.views.append(
                View(
                    route="/register",
                    controls=[
                        AppBar(title=Text("Authorization", size=15)),
                        Text(value="Registration", size=30),
                        username := TextField(label="Username", width=300, max_length=20),
                        password := TextField(label="Password", password=True, can_reveal_password=True, width=300, max_length=80),
                        ElevatedButton(text="Register", on_click=register),
                        log_message := Text()
                    ],
                    vertical_alignment=MainAxisAlignment.CENTER,
                    horizontal_alignment=CrossAxisAlignment.CENTER,
                    spacing=10
                )
            )
