from aiogram import types

from app import MyBot
from apps.core.bot.callbacks.sequential_action.data_answer import get_and_send_main_category_data
from apps.core.bot.data.category import get_data_list
from apps.core.bot.reports.report_data_preparation import set_violation_atr_data
from loader import logger

logger.debug("main_category_answer")


@MyBot.dp.callback_query_handler(lambda call: call.data in get_data_list("MAIN_CATEGORY"))
async def main_category_answer(call: types.CallbackQuery):
    """Обработка ответов содержащихся в MAIN_CATEGORY
    """
    if call.data in get_data_list("MAIN_CATEGORY"):
        try:

            await set_violation_atr_data("main_category", call.data)
            await get_and_send_main_category_data(call)

        except Exception as callback_err:
            logger.error(f"{repr(callback_err)}")
