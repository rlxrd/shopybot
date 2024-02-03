from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command

import app.keyboards as kb
from app.database.requests import get_item_by_id

router = Router()


@router.message(CommandStart())
@router.callback_query(F.data == 'to_main')
async def cmd_start(message: Message | CallbackQuery):
    if isinstance(message, Message):
        await message.answer("Добро пожаловать в интернет магазин!",
                             reply_markup=kb.main)
    else:
        await message.message.edit_text("Добро пожаловать в интернет магазин!",
                                        reply_markup=kb.main)


@router.callback_query(F.data == 'catalog')
async def catalog(callback: CallbackQuery):
    await callback.answer('')
    await callback.message.edit_text(text='Выберите категорию.',
                                     reply_markup=await kb.categories())


@router.callback_query(F.data.startswith('category_'))
async def category(callback: CallbackQuery):
    await callback.answer('')
    await callback.message.edit_text('Выберите товар',
                                     reply_markup=await kb.items(callback.data.split('_')[1]))


@router.callback_query(F.data.startswith('item_'))
async def category(callback: CallbackQuery):
    item = await get_item_by_id(callback.data.split('_')[1])
    await callback.answer('')
    await callback.message.edit_text(f'{item.name}\n\n{item.description}\n\nЦена: {item.price} рублей',
                                     reply_markup=kb.to_main)
