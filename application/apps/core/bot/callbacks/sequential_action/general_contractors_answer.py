from apps.core.bot.callbacks.sequential_action.data_answer import get_and_send_general_contractors_data
from apps.core.bot.reports.report_data_preparation import set_violation_atr_data
from loader import logger

logger.debug(f"{__name__} start import")
from aiogram import types
from apps.core.bot.callbacks.sequential_action.category import get_data_list
from aiogram.dispatcher import FSMContext
from apps.core.bot.reports.report_data import ViolationData
from apps.core.database.db_utils import db_get_full_title
from apps.core.database.transformation_category import CATEGORY_ID_TRANSFORM
from apps.MyBot import MyBot

logger.debug(f"{__name__} finish import")


@MyBot.dp.callback_query_handler(lambda call: call.data in get_data_list("GENERAL_CONTRACTORS"),
                                 state=ViolationData.all_states)
async def general_contractors_answer(call: types.CallbackQuery, state: FSMContext = None):
    """Обработка ответов содержащихся в GENERAL_CONTRACTORS
    """
    try:
        value: str = await db_get_full_title(
            table_name=CATEGORY_ID_TRANSFORM['general_contractor']['table'],
            short_title=call.data
        )

        await set_violation_atr_data("general_contractor", value, state=state)

        await get_and_send_general_contractors_data(call, state=state)

    except Exception as callback_err:
        logger.error(f"{repr(callback_err)}")
