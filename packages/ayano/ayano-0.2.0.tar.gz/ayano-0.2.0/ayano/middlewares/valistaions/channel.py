from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message, CallbackQuery

from ayano.utils import validation


class InChannelValidationMiddleware(BaseMiddleware):
    def __init__(self, channel_id: int):
        self.channel_id = channel_id
        super().__init__()

    async def __call__(
            self,
            handler: Callable[
                [TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any],
    ) -> Any:
        if isinstance(event, Message) or isinstance(event, CallbackQuery):
            in_channel = await validation.in_group(
                bot=event.bot,
                user_id=event.from_user.id,
                group_id=self.channel_id,
            )
            if not in_channel:
                return
        else:
            return

        return await handler(event, data)
