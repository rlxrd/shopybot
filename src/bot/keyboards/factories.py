from aiogram.filters.callback_data import CallbackData


class ShopFactory(CallbackData, prefix="shop"):
    nav: str


class CategoryFactory(CallbackData, prefix="category"):
    id: int


class ItemFactory(CallbackData, prefix="item"):
    id: int


class AdminFactory(CallbackData, prefix="admin"):
    action: str
    value: str | None = None