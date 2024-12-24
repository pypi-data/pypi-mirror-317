from aiogram.utils.keyboard import CallbackData


class PaginationCallbackData(CallbackData, prefix="pagination"):
    name: str
    offset: int
    limit: int


class PaginationSelectCallbackData(CallbackData, prefix="pag-answer"):
    name: str
    value: str
    offset: int
    limit: int


class PaginationBackCallbackData(CallbackData, prefix="pag-back"):
    name: str
