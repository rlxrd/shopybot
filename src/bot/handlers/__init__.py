from aiogram import Router
from .admin import AdminPanel


def setup_message_routers() -> Router:
    from . import start, admin

    router = Router()
    router.include_router(start.router)
    router.include_router(admin.router)
    return router