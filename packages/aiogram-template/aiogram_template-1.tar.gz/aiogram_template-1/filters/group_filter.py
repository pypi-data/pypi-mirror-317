from aiogram.types import Message
from aiogram.filters import BaseFilter

class IsGroupMessage(BaseFilter):
    """
    Bu filter faqat guruhdagi yoki superguruhdagi xabarlarni aniqlash uchun ishlaydi.
    """

    async def __call__(self, message: Message) -> bool:
        """
        Agar xabar guruh yoki superguruhdan yuborilgan bo'lsa, True qaytaradi.
        """
        return message.chat.type in ["group", "supergroup"]
