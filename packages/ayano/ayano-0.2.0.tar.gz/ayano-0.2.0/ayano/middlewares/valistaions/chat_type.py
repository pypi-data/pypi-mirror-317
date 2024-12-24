from dataclasses import dataclass
from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject


@dataclass
class AiogramChatTypes:
    private: str = "private"
    sender: str = "sender"
    group: str = "group"
    supergroup: str = "supergroup"
    channel: str = "channel"


class ChatTypeValidationMiddleware(BaseMiddleware):
    def __init__(self, *chat_types):
        super().__init__()
        self.chat_types = chat_types

    async def __call__(
            self,
            handler: Callable[
                [TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any],
    ) -> Any:
        if event.chat.type not in self.chat_types:
            return

        return await handler(event, data)
