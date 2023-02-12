from loader import logger

logger.debug(f"{__name__} start import")
import asyncio

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from apps.xxx import assistant
from config.config import ADMINS_ID
from loader import logger

logger.debug(f"{__name__} finish import")


async def admin_notify(user_id, notify_text: str, button: InlineKeyboardButton = None) -> bool:
    """Уведомление админов
    """

    logger.info(notify_text)
    try:
        reply_markup = InlineKeyboardMarkup()
        reply_markup.add(
            InlineKeyboardButton(text=f'{user_id}', url=f"tg://user?id={user_id}")
        )
        if button:
            reply_markup.add(button)

        for bot_admin in ADMINS_ID:
            await assistant.send_message(chat_id=bot_admin,
                                         text=notify_text,
                                         reply_markup=reply_markup)
        return True
    except Exception as err:
        logger.error(f'User {user_id} ошибка уведомления ADMIN_ID {repr(err)}')
        return False


async def test2():
    user_id: str = '373084462'
    notify_text: str = f'User {user_id} попытка доступа к функциям без регистрации'
    button = InlineKeyboardButton(text=f'{user_id}', url=f"tg://user?id={user_id}")
    answer: bool = await admin_notify(user_id, notify_text, button)

    print(answer)


if __name__ == "__main__":
    asyncio.run(test2())
