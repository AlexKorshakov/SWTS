from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.exceptions import ChatNotFound
from loader import logger

from aiogram import Dispatcher
from asyncio import sleep

from config.config import ADMIN_ID


async def on_startup_notify(dp: Dispatcher):
    logger.info("Оповещение администрации...")
    # for admin_id in ADMINS_ID:

    try:
        await dp.bot.send_message(ADMIN_ID, "Бот был успешно запущен", disable_notification=True)
        logger.info(f"Сообщение отправлено {ADMIN_ID}")
    except Exception as err:
        logger.error(f"Чат с админом не найден {err} ")

    await sleep(0.3)


async def admin_notify(user_id, notify_text) -> None:
    """Уведомление админов"""

    logger.info(notify_text)

    try:
        reply_markup = InlineKeyboardMarkup()
        reply_markup.add(
            InlineKeyboardButton(text=f'{user_id}', url=f"tg://user?id={user_id}")
        )

        # await MyBot.dp.bot.send_message(chat_id=ADMIN_ID,
        #                                 text=notify_text,
        #                                 reply_markup=reply_markup)
    except Exception:
        logger.info(f'User {user_id} ошибка уведомления ADMIN_ID')
