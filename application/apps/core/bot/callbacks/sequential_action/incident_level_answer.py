from apps.core.bot.reports.report_data_preparation import set_violation_atr_data
from loader import logger

logger.debug(f"{__name__} start import")
from aiogram import types
from aiogram.dispatcher import FSMContext
from apps.core.bot.reports.report_data import ViolationData
from apps.core.bot.callbacks.sequential_action.data_answer import get_and_send_incident_level_data
from apps.core.bot.callbacks.sequential_action.category import get_data_list
from apps.MyBot import MyBot

logger.debug(f"{__name__} finish import")


@MyBot.dp.callback_query_handler(lambda call: call.data in get_data_list("INCIDENT_LEVEL"),
                                 state=ViolationData.all_states)
async def incident_level(call: types.CallbackQuery, state: FSMContext = None):
    """Обработка ответов содержащихся в INCIDENT_LEVEL
    """
    if call.data in get_data_list("INCIDENT_LEVEL"):
        try:

            await set_violation_atr_data("incident_level", call.data, state=state)

            await get_and_send_incident_level_data(call)

        except Exception as callback_err:
            logger.error(f"{repr(callback_err)}")
