from loader import logger

logger.debug(f"{__name__} start import")
from aiogram import types
from aiogram.dispatcher import FSMContext
from apps.core.bot.reports.report_data_preparation import set_violation_atr_data
from apps.core.bot.reports.report_data import ViolationData
from apps.core.bot.callbacks.sequential_action.data_answer import get_and_send_violation_category_data
from apps.core.bot.callbacks.sequential_action.category import get_data_list
from apps.MyBot import MyBot

logger.debug(f"{__name__} finish import")


@MyBot.dp.callback_query_handler(lambda call: call.data in get_data_list("VIOLATION_CATEGORY"),
                                 state=ViolationData.all_states)
async def violation_category_answer(call: types.CallbackQuery, state: FSMContext = None):
    """Обработка ответов содержащихся в VIOLATION_CATEGORY
    """
    try:

        await set_violation_atr_data("violation_category", call.data, state=state)

        await get_and_send_violation_category_data(call, state=state)

    except Exception as callback_err:
        logger.error(f"{repr(callback_err)}")
