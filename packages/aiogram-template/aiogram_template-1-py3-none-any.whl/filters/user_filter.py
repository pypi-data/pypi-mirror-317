from aiogram.types import Message
from aiogram.filters import BaseFilter

class IsUserMessage(BaseFilter):
    """
    Bu filter faqat foydalanuvchidan kelgan xabarlarni aniqlash uchun ishlaydi.
    """

    async def __call__(self, message: Message) -> bool:
        """
        Agar xabar foydalanuvchidan yuborilgan bo'lsa, True qaytaradi.
        """
        return message.from_user is not None
