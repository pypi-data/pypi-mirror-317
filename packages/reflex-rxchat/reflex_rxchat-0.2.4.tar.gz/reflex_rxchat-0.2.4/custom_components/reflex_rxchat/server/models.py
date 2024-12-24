import reflex as rx

from .events import Message


class Conversation(rx.Model):
    id: str
    title: str
    usernames: list[str] = []
    messages: list[Message] = []

    def add_message(self, message: Message):
        if message.username not in self.usernames:
            self.usernames.append(message.username)
        self.messages.append(message)

    def remove_user(self, username: str):
        self.usernames.remove(username)

    def user_count(self) -> int:
        return len([username for username in self.usernames if username != "_system"])

    def tail(self, num_messages: int) -> "Conversation":
        return Conversation(
            id=self.id,
            title=self.title,
            usernames=self.usernames,
            messages=self.messages[:num_messages],
        )
