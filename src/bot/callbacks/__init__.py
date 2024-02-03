from aiogram import Router


def setup_callback_routers() -> Router:
    from . import shop

    router = Router()
    router.include_router(shop.router)
    return router