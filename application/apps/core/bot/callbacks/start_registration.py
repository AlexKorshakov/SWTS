from aiogram import types

from app import MyBot
from loader import logger

logger.debug("start_registration")
from apps.core.bot.callbacks.callback_action import cb_start
from apps.core.bot.data.category import get_data_list
from apps.core.bot.keyboards.inline.select_category import bild_inlinekeyboar


@MyBot.dp.callback_query_handler(cb_start.filter(action=["start_registration"]))
async def callbacks_start_registration(call: types.CallbackQuery, callback_data: dict):
    """Обработка действия action из фабрики Callback cb_start
    """
    action = callback_data["action"]
    if action == "start_registration":
        logger.info(f'User @{call.message.chat.username}:{call.message.chat.id} начало регистрации')
        await bild_inlinekeyboar(call.message, some_list=get_data_list("MAIN_LOCATIONS"))
    await call.answer()
