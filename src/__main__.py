import asyncio
import logging
from contextlib import suppress

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.scene import SceneRegistry
from aiogram.fsm.storage.memory import SimpleEventIsolation

from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession, AsyncEngine

from bot.middlewares import DBSessionMiddleware
from bot.handlers import AdminPanel
from bot.handlers import setup_message_routers
from bot.callbacks import setup_callback_routers

from db import Base
from config_reader import config


async def on_startup(_engine: AsyncEngine) -> None:
    async with _engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)


async def on_shutdown(bot: Bot, session: AsyncSession) -> None:
    await bot.session.close()
    await session.close()


async def main() -> None:
    _engine = create_async_engine(config.DATABASE_URL.get_secret_value())
    sessionmaker = async_sessionmaker(_engine, expire_on_commit=False)

    bot = Bot(config.BOT_TOKEN.get_secret_value(), parse_mode=ParseMode.HTML)
    dp = Dispatcher(_engine=_engine, events_isolation=SimpleEventIsolation())

    dp.update.middleware(DBSessionMiddleware(sessionmaker))

    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    message_routers = setup_message_routers()
    callback_routers = setup_callback_routers()
    dp.include_router(message_routers)
    dp.include_router(callback_routers)

    scene_registry = SceneRegistry(dp)
    scene_registry.add(AdminPanel)

    await bot.delete_webhook(True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    with suppress(KeyboardInterrupt):
        asyncio.run(main())
