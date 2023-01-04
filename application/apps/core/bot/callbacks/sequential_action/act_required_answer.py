from aiogram import types

from apps.MyBot import MyBot
from apps.core.bot.callbacks.sequential_action.data_answer import get_and_send_act_required_data
from apps.core.bot.data.category import get_data_list
from apps.core.bot.reports.report_data_preparation import set_violation_atr_data
from loader import logger

logger.debug("act_required")


@MyBot.dp.callback_query_handler(lambda call: call.data in get_data_list("ACT_REQUIRED"))
async def act_required_answer(call: types.CallbackQuery):
    """Обработка ответов содержащихся в ACT_REQUIRED
    """
    if call.data in get_data_list("ACT_REQUIRED"):
        try:

            await set_violation_atr_data("act_required", call.data)

            await get_and_send_act_required_data(call)

        except Exception as callback_err:
            logger.error(f"{repr(callback_err)}")
