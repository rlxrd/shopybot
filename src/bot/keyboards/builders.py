from aiogram.utils.keyboard import InlineKeyboardBuilder
from sqlalchemy import ScalarResult

from .factories import CategoryFactory, ItemFactory


def category_builder(category_list: list[ScalarResult]) -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    [
        builder.button(text=category.name, callback_data=CategoryFactory(id=category.id).pack())
        for category in category_list
    ]
    return builder.adjust(2).as_markup()


def item_builder(item_list: list[ScalarResult]) -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    [
        builder.button(text=item.name, callback_data=ItemFactory(id=item.id).pack())
        for item in item_list
    ]
    return builder.adjust(2).as_markup()


# Вообще я думаю можно все сделать in one func. и хз зачем ID в CategoryFactory