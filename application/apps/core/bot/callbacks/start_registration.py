from loader import logger

logger.debug(f"{__name__} start import")
from aiogram import types
from apps.core.bot.callbacks.callback_action import cb_start
from apps.core.bot.callbacks.sequential_action.data_answer import \
    get_and_send_start_main_locations_data
from apps.MyBot import MyBot

logger.debug(f"{__name__} finish import")


@MyBot.dp.callback_query_handler(cb_start.filter(action=["start_registration"]))
async def callbacks_start_registration(call: types.CallbackQuery, callback_data: dict):
    """Обработка действия action из фабрики Callback cb_start
    """

    action = callback_data["action"]
    if action == "start_registration":
        logger.info(f'User @{call.message.chat.username}:{call.message.chat.id} начало регистрации')

        await get_and_send_start_main_locations_data(call, callback_data)
