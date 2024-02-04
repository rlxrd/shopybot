from dataclasses import dataclass

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.scene import Scene, on
from aiogram.fsm.context import FSMContext

from bot.keyboards import AdminFactory
from bot.keyboards import admin_markup

from config_reader import config


@dataclass
class Container:
    text: str


ADD_ITEM_MODEL = [
    Container("Название товара"),
    Container("Описание товара"),
    Container("Фото товара"),
    Container("Цена товара"),
    Container("Категория товара")
]

DELETE_ITEM_MODEL = [
    Container("ID товара")
]


class AdminPanel(Scene):

    @on.message.enter()
    async def on_enter(self, message: Message, state: FSMContext, step: int | None = 0) -> None:
        if not step:
            await message.answer("Админ панель", reply_markup=admin_markup)
        await state.update_data(step=step)

    @on.message.exit()
    async def on_exit(self, message: Message, state: FSMContext) -> None:
        await state.clear()

    @on.callback_query(AdminFactory.filter(F.action))
    async def admin_action(
        self, query: CallbackQuery, callback_data: AdminFactory, state: FSMContext
    ) -> None:
        match callback_data.action:
            case "add-item": text = "Процесс добавления товара. Отмена - /cancel"
            case "delete-item": text = "Процесс удаления товара. Отмена - /cancel"

        await query.answer()
        await state.update_data(action=callback_data.action)
        await query.message.answer(text)

    @on.message(Command("cancel"))
    async def cancel(self, message: Message, state: FSMContext) -> None:
        if await state.get_state():
            await state.clear()

    @on.message(F.text)
    async def process_text(self, message: Message, state: FSMContext) -> None:
        data = await state.get_data()
        step = data["step"]

        await message.answer("test")
        await state.update_data(text=message.text)
        await self.wizard.retake(step=step + 1)


router = Router()
router.message.filter(F.from_user.id.in_(config.ADMIN_IDS))
router.message.register(AdminPanel.as_handler(), Command("panel"))

# TODO: Дописать...