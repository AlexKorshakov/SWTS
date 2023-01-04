from aiogram import types

from apps.MyBot import MyBot
from apps.core.bot.callbacks.sequential_action.data_answer import get_and_send_elimination_time_data
from apps.core.bot.data.category import get_data_list
from apps.core.bot.reports.report_data_preparation import set_violation_atr_data
from loader import logger

logger.debug("elimination_time_answer")


@MyBot.dp.callback_query_handler(lambda call: call.data in get_data_list("ELIMINATION_TIME"))
async def elimination_time_answer(call: types.CallbackQuery):
    """Обработка ответов содержащихся в ELIMINATION_TIME
    """
    if call.data in get_data_list("ELIMINATION_TIME"):
        try:
            await set_violation_atr_data("elimination_time", call.data)

            await get_and_send_elimination_time_data(call)

        except Exception as callback_err:
            logger.error(f"{repr(callback_err)}")
