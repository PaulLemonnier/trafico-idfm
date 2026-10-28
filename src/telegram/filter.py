from aiogram.types import Message

from src.config import settings


ALLOWED_CHAT_ID = int(settings.ALLOWED_CHAT_ID)

def is_allowed(message: Message) -> bool:
    return (
        message.chat.id == ALLOWED_CHAT_ID
        and message.sender_chat is not None
        and message.sender_chat.id == ALLOWED_CHAT_ID
    )