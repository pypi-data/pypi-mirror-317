from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram import Router, html

# Router yaratish
router = Router()

@router.message(CommandStart())  # /start komandasi uchun handler
async def command_start_handler(message: Message) -> None:
    """
    /start komandasi yuborilganida bu funksiyaga kiritiladi
    """
    # Foydalanuvchiga salom yuborish, ismini qalin qilib ko'rsatish
    await message.answer(f"Salom, {html.bold(message.from_user.full_name)}!")
