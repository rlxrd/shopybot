from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from .factories import ShopFactory, AdminFactory

main_markup = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Каталог", callback_data=ShopFactory(nav="catalog").pack())
        ],
        [
            InlineKeyboardButton(text="Корзина", callback_data=ShopFactory(nav="basket").pack()),
            InlineKeyboardButton(text="Контакты", callback_data=ShopFactory(nav="contacts").pack())
        ]
    ]
)

back_to_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="В главное меню", callback_data="main_menu")]
    ]
)

admin_markup = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Добавить товар", callback_data=AdminFactory(action="add-item").pack()
            ),
            InlineKeyboardButton(
                text="Удалить товар", callback_data=AdminFactory(action="delete-item").pack()
            )
        ]
    ]       
)