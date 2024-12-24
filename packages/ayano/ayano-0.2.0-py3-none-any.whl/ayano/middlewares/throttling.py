import time
from collections import defaultdict, deque
from typing import Callable, Awaitable, Dict, Any

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject


class ThrottlingMiddleware(BaseMiddleware):
    def __init__(self, limit_per_second: int = 4):
        """
        Миддлваре для установки лимита на кол-во запросов в секунду
        :param limit_per_second: лимит запросов в секунду
        """
        super().__init__()
        self.requests = defaultdict(deque)
        self.limit = limit_per_second

    async def __call__(
            self,
            handler: Callable[
                [TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any],
    ) -> Any:
        user_id = event.from_user.id

        while self.requests[user_id] and self.requests[user_id][0] + 1 < time.time():
            self.requests[user_id].popleft()

        self.requests[user_id].append(time.time())
        if len(self.requests[user_id]) > self.limit:
            return

        return await handler(event, data)
