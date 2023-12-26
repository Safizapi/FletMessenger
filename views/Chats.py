from flet import Page, View, Text, CrossAxisAlignment, Container, Row, TextField, ElevatedButton, UserControl, Column
from flet import ScrollMode
from Additional.Sidebar import Sidebar
import sqlite3 as sql
import json
import socket
import time

conn = sql.connect("appDB.db")
db = conn.cursor()

with open("username.txt") as file:
    username = list(db.execute("SELECT * FROM users WHERE id=?", (file.readlines()[1],)))[0][1]


class Chats:
    def __init__(self, page: Page):
        self.page = page

    def chats_page(self) -> None:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        s.bind(("0.0.0.0", 11719))

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

        # Send message to chat
        def send_message(e: UserControl) -> None:
            if message.value and not set(message.value) == {" "}:
                sock.sendto(f"{username}\n{message.value}".encode(), ("255.255.255.255", 11719))
                x.insert(-1, Row([Text(f"{username}\n{message.value}", width=400)]))

                with open("messagelog.json", "r") as log:
                    messages = json.load(log)

                with open("messagelog.json", "w") as log:
                    messages[username + ' ' + str(time.time())] = message.value
                    log.write(json.dumps(messages, indent=2))

            message.value = ""
            self.page.update()

        # Receive message from other users (unused because I didn't find the way to make a loop for this)
        def receive_message() -> None:
            while True:
                messg = s.recv(64000).decode()
                x.insert(-1, Row([Text(f"{messg}", width=400)]))
                self.page.update()

        # Creating page
        if self.page.route == "/chats":
            screen = Container(
                expand=True,
                content=Column(x := [Row([
                    message := TextField(label="Message", max_length=1000, max_lines=5, autofocus=True),
                    ElevatedButton(text="Send", on_click=send_message)
                ])], scroll=ScrollMode.AUTO)
            )

            with open("messagelog.json", "r") as logs:
                for i in json.load(logs).items():
                    x.insert(-1, Row([Text(f"{i[0].split()[0]}\n{i[1]}", width=400)]))

            self.page.views.append(
                View(
                    route="/chats",
                    controls=[
                        Text(value="Chats", size=20),
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
