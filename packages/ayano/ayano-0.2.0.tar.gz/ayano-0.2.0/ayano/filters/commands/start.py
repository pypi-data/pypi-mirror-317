from aiogram import types
from aiogram.filters import BaseFilter
from ayano.exceptions.filters import CompareFuncNotFoundError


class DefaultStartCommand(BaseFilter):
    async def __call__(self, message: types.Message, *args, **kwargs) -> bool:
        if not message.text:
            return False

        return message.text == "/start"


class StartWithPayload(BaseFilter):
    check_funcs = {
        "startswith": lambda message_data, prefix: message_data.startswith(prefix),
        "equal": lambda message_data, prefix: message_data == prefix,
        "endswith": lambda message_data, prefix: message_data.endswith(prefix),
        "in": lambda message_data, prefix: prefix in message_data,
    }

    def __init__(self, prefix: str, compare_func: str = "startswith"):
        self.prefix = prefix
        if compare_func not in self.check_funcs:
            raise CompareFuncNotFoundError(compare_func)

        self.check_func = self.check_funcs[compare_func]

    async def __call__(self, message: types.Message, *args, **kwargs) -> bool:
        if not message.text:
            return False
        data = message.text.split(' ')

        return len(data) == 2 and data[0] == '/start' and self.check_func(data[1], self.prefix)
