from aiogram import types
from loader import logger

from app import MyBot
from apps.core.bot.callbacks.sequential_action.data_answer import get_and_send_main_locations_data, \
    get_and_send_start_main_locations_data
from apps.core.bot.callbacks.callback_action import cb_start

logger.debug("start_registration")


@MyBot.dp.callback_query_handler(cb_start.filter(action=["start_registration"]))
async def callbacks_start_registration(call: types.CallbackQuery, callback_data: dict):
    """Обработка действия action из фабрики Callback cb_start
    """

    action = callback_data["action"]
    if action == "start_registration":
        logger.info(f'User @{call.message.chat.username}:{call.message.chat.id} начало регистрации')

        await get_and_send_start_main_locations_data(call, callback_data)
