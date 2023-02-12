from asyncio import sleep

from aiogram import Dispatcher
from config.config import ADMIN_ID
from loader import logger


async def on_startup_notify(dp: Dispatcher):
    logger.info("Оповещение администрации...")
    # for admin_id in ADMINS_ID:

    try:
        await dp.bot.send_message(ADMIN_ID, "Бот был успешно запущен", disable_notification=True)
        logger.info(f"Сообщение отправлено {ADMIN_ID}")
    except Exception as err:
        logger.error(f"Чат с админом не найден {err} ")

    await sleep(0.3)


