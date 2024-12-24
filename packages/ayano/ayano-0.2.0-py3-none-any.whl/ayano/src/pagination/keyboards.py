from aiogram.utils.keyboard import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardBuilder,
)

from .callbacks import (
    PaginationCallbackData,
    PaginationSelectCallbackData,
    PaginationBackCallbackData
)


def pagination_keyboard(
        name: str,
        offset: int,
        limit: int,
        buttons_text: list[str],
        buttons_callback: list[str],
        add_back_button: bool = True,
) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    for text, callback in zip(buttons_text, buttons_callback):
        builder.row(InlineKeyboardButton(
            text=text,
            callback_data=PaginationSelectCallbackData(
                name=name,
                value=callback,
                offset=offset,
                limit=limit,
            ).pack(),
        ))

    if offset > 0:
        builder.row(InlineKeyboardButton(
            text="<<<",
            callback_data=PaginationCallbackData(
                name=name,
                offset=offset - limit if offset - limit >= 0 else 0,
                limit=limit,
            ).pack(),
        ))
    if len(buttons_text) == limit:
        button = InlineKeyboardButton(
            text=">>>",
            callback_data=PaginationCallbackData(
                name=name,
                offset=offset + limit,
                limit=limit,
            ).pack(),
        )
        if offset > 0:
            builder.add(button)
        else:
            builder.row(button)

    if add_back_button:
        builder.row(InlineKeyboardButton(
            text="↩️ Назад",
            callback_data=PaginationSelectCallbackData(
                name=name,
                value="__back",
                offset=offset,
                limit=limit,
            ).pack(),
        ))

    return builder.as_markup()


def pagination_select_back(
        base_keyboard: InlineKeyboardMarkup,
        name: str,
        offset: int,
        limit: int
) -> InlineKeyboardMarkup:
    base_keyboard.inline_keyboard.append([InlineKeyboardButton(
        text="↩️ Назад",
        callback_data=PaginationCallbackData(
            name=name,
            offset=offset,
            limit=limit,
        ).pack()
    )])
    return base_keyboard
