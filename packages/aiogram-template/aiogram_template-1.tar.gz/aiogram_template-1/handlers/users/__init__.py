from aiogram import Dispatcher
from .users import router as user_router

def setup(dp: Dispatcher):
    """
    Botning routerlarini ulash uchun setup funksiyasi.
    """
    dp.include_routers(
        user_router  # Foydalanuvchi bilan bog'liq handlerlar
    )
