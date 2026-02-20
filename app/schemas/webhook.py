from pydantic import BaseModel


class Chat(BaseModel):
    id: int


class Message(BaseModel):
    message_id: int
    chat: Chat
    text: str | None = None


class TelegramWebhook(BaseModel):
    update_id: int
    message: Message | None = None
