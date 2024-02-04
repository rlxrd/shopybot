from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command, Filter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

import app.keyboards as kb
from app.database.requests import get_users, set_item

admin = Router()


class Newsletter(StatesGroup):
    message = State()


class AddItem(StatesGroup):
    name = State()
    category = State()
    description = State()
    photo = State()
    price = State()


class AdminProtect(Filter):
    async def __call__(self, message: Message):
        return message.from_user.id in [5791374868]


@admin.message(AdminProtect(), Command('apanel'))
async def apanel(message: Message):
    await message.answer('Возможные команды: /newsletter\n/add_item')


@admin.message(AdminProtect(), Command('newsletter'))
async def newsletter(message: Message, state: FSMContext):
    await state.set_state(Newsletter.message)
    await message.answer('Отправьте сообщение, которое вы хотите разослать всем пользователям')
    

@admin.message(AdminProtect(), Newsletter.message)
async def newsletter_message(message: Message, state: FSMContext):
    await message.answer('Подождите... идёт рассылка.')
    for user in await get_users():
        try:
            await message.send_copy(chat_id=user.tg_id)
        except:
            pass
    await message.answer('Рассылка успешно завершена.')
    await state.clear()


@admin.message(AdminProtect(), Command('add_item'))
async def add_item(message: Message, state: FSMContext):
    await state.set_state(AddItem.name)
    await message.answer('Введите название товара')


@admin.message(AdminProtect(), AddItem.name)
async def add_item_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(AddItem.category)
    await message.answer('Выберите категорию товара', reply_markup=await kb.categories())


@admin.callback_query(AdminProtect(), AddItem.category)
async def add_item_category(callback: CallbackQuery, state: FSMContext):
    await state.update_data(category=callback.data.split('_')[1])
    await state.set_state(AddItem.description)
    await callback.answer('')
    await callback.message.answer('Введите описание товара')


@admin.message(AdminProtect(), AddItem.description)
async def add_item_description(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    await state.set_state(AddItem.photo)
    await message.answer('Отправьте фото товара')


@admin.message(AdminProtect(), AddItem.photo, F.photo)
async def add_item_photo(message: Message, state: FSMContext):
    await state.update_data(photo=message.photo[-1].file_id)
    await state.set_state(AddItem.price)
    await message.answer('Введите цену товара')


@admin.message(AdminProtect(), AddItem.price)
async def add_item_price(message: Message, state: FSMContext):
    await state.update_data(price=message.text)
    data = await state.get_data()
    await set_item(data)
    await message.answer('Товар успешно добавлен')
    await state.clear()
