from aiogram.dispatcher import FSMContext

from apps.core.bot.callbacks.callback_action import cb_start
from apps.core.bot.reports.report_data import ViolationData
from loader import logger

logger.debug(f"{__name__} start import")
from aiogram import types
from apps.core.bot.callbacks.sequential_action.data_answer import get_and_send_start_main_locations_data
from apps.MyBot import MyBot

logger.debug(f"{__name__} finish import")


@MyBot.dp.callback_query_handler(cb_start.filter(action=['select_start_registration']), state=ViolationData.all_states)
async def callbacks_start_registration(call: types.CallbackQuery, callback_data: dict, state: FSMContext = None):
    """Обработка действия action из фабрики Callback cb_start
    """

    logger.info(f'User @{call.message.chat.username}:{call.message.chat.id} начало регистрации')

    await get_and_send_start_main_locations_data(call, data_answer='Зарегистрировать', state=state)
