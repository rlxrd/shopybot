from aiogram import Router


def setup_message_routers() -> Router:
    from . import start

    router = Router()
    router.include_router(start.router)
    return router