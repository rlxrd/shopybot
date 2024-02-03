from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from bot.keyboards import main_markup
from db import User

router = Router()


@router.message(CommandStart())
@router.callback_query(F.data == "main_menu")
async def start(message: Message | CallbackQuery, session: AsyncSession) -> None:
    user = await session.scalar(select(User).where(User.tg_id == message.from_user.id))
    if not user:
        session.add(User(tg_id=message.from_user.id))
        await session.commit()

    pattern = {
        "text": "Добро пожаловать в главное меню!",
        "reply_markup": main_markup
    }

    if isinstance(message, CallbackQuery):
        await message.answer()
        await message.message.edit_text(**pattern)
    else:
        await message.answer(**pattern)


# Other commands for user...
