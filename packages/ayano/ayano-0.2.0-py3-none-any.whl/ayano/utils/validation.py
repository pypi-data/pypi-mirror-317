from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest, TelegramForbiddenError


async def in_group(bot: Bot, user_id: int, group_id: int) -> bool:
    try:
        user = await bot.get_chat_member(group_id, user_id)
        return user.status != "left"
    except (TelegramBadRequest, TelegramForbiddenError):
        return False
