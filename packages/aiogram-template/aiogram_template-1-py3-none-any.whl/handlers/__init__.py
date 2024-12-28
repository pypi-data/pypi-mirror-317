from aiogram import Dispatcher

from handlers import users, admin  # users va admin moduli import qilinadi

def setup(dp: Dispatcher):
    """
    Botning routerlarini sozlash uchun setup funksiyasi.
    """
    users.setup(dp)  # Foydalanuvchi bilan bog'liq handlerlarni ulash
    admin.setup(dp) # Adminlar bilan bog'liq handlerlarni ulash
