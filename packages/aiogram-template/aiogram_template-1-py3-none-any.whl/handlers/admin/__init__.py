from aiogram import Dispatcher
from .admin import router as admin_router

def setup(dp: Dispatcher):
    """
    Botning routerlarini ulash uchun setup funksiyasi.
    """
    dp.include_routers(
        admin_router  # Adminlar bilan bog'liq handlerlar
    )
