from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from .factories import ShopFactory

main_markup = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Каталог", callback_data=ShopFactory(nav="catalog").pack())
        ],
        [
            InlineKeyboardButton(text="Каталог", callback_data=ShopFactory(nav="basket").pack()),
            InlineKeyboardButton(text="Каталог", callback_data=ShopFactory(nav="contacts").pack())
        ]
    ]
)

back_to_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="В главное меню", callback_data="main_menu")]
    ]
)
