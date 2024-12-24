from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message, CallbackQuery


class CompareAttrsMiddleware(BaseMiddleware):
    def __init__(
            self,
            user_model_middleware_name: str,
            user_model_attr_name: str,
            user_model_attr_value: Any,
    ):
        """
        Получает объект из предыдущих прослоек с названием
        <user_model_middleware_name> и сравнивает аттрибут
        <user_model_attr_name> со значением <user_model_attr_value>

        Пример:
        user_model_middleware_name = "user"
        user_model_attr_name = "is_block"
        user_model_attr_value = "True"

        В таком случает, если у user есть is_block=True,
        миддлвари не пропустит дальше

        :param user_model_middleware_name:
        :param user_model_attr_name:
        :param user_model_attr_value:
        """
        super().__init__()
        self.user_model_middleware_name = user_model_middleware_name
        self.user_model_attr_name = user_model_attr_name
        self.user_model_attr_value = user_model_attr_value

    async def __call__(
            self,
            handler: Callable[
                [TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any],
    ) -> Any:
        user: Any = data.get(self.user_model_middleware_name)
        if getattr(user, self.user_model_attr_name) == self.user_model_attr_value:
            return

        return await handler(event, data)
