from aiogram import Router, F
from aiogram.types import CallbackQuery

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from bot.keyboards import ShopFactory, CategoryFactory, ItemFactory
from bot.keyboards import markup_builder, back_to_menu
from db import Category, Item

router = Router()


@router.callback_query(ShopFactory.filter(F.nav))
async def navigation_menu(
    query: CallbackQuery, callback_data: ShopFactory, session: AsyncSession
) -> None:
    pattern = {}
    if callback_data.nav == "catalog":
        all_categories = await session.scalars(select(Category))
        pattern["text"] = "Выберите категорию"
        pattern["reply_markup"] = markup_builder(all_categories)

    await query.answer()
    await query.message.edit_text(**pattern)


@router.callback_query(CategoryFactory.filter(F.id))
async def category_items(
    query: CallbackQuery, callback_data: CategoryFactory, session: AsyncSession
) -> None:
    items = await session.scalars(select(Item))
    await query.answer()
    await query.message.edit_text("Выберите товар", reply_markup=markup_builder(items, "item"))


@router.callback_query(ItemFactory.filter(F.id))
async def show_item(
    query: CallbackQuery, callback_data: ItemFactory, session: AsyncSession
) -> None:
    item = await session.scalar(select(Item).where(Item.id == callback_data.id))
    await query.answer()
    await query.message.edit_text(
        f"<b>{item.name}</b> (<code>{item.price:,}</code> 💲)\n<i>{item.description}</i>",
        reply_markup=back_to_menu
    )