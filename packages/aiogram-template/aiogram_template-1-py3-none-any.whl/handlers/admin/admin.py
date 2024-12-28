# start admin code writing
from aiogram.filters import Command
from aiogram.types import Message
from aiogram import Router, F

from data.config import ADMINS
from filters.admin_filter import IsAdmin

router =  Router()

@router.message(Command(commands=['admin','panel']), IsAdmin(user_ids=7268580213))
async def admin_panel(messge: Message):
    await messge.answer(
        text="Assalomu Alaykum admin panelga xush kelibsiz"
    )
