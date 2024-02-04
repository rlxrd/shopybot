from aiogram.utils.keyboard import InlineKeyboardBuilder
from sqlalchemy import ScalarResult

from .factories import CategoryFactory, ItemFactory


def markup_builder(item_list: list[ScalarResult], table: str = "category") -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()

    match table:
        case "category": _factory = CategoryFactory
        case "item": _factory = ItemFactory

    [
        builder.button(text=item.name, callback_data=_factory(id=item.id).pack())
        for item in item_list
    ]
    return builder.adjust(2).as_markup()