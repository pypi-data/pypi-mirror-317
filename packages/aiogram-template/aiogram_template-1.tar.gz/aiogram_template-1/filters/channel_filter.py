from aiogram.types import Message
from aiogram.filters import BaseFilter

class IsChannelMessage(BaseFilter):
    """
    Bu filter faqat kanaldagi xabarlarni aniqlash uchun ishlaydi.
    """

    async def __call__(self, message: Message) -> bool:
        """
        Agar xabar kanaldan yuborilgan bo'lsa, True qaytaradi.
        """
        return message.chat.type == "channel"
