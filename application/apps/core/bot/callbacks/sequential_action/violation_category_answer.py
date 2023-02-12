from loader import logger

logger.debug(f"{__name__} start import")
from aiogram import types
from apps.core.bot.callbacks.sequential_action.data_answer import \
    get_and_send_violation_category_data
from apps.core.bot.data.category import get_data_list
from apps.core.bot.reports.report_data import violation_data
from apps.core.utils.json_worker.writer_json_file import write_json_file
from apps.MyBot import MyBot

logger.debug(f"{__name__} finish import")


@MyBot.dp.callback_query_handler(lambda call: call.data in get_data_list("VIOLATION_CATEGORY"))
async def violation_category_answer(call: types.CallbackQuery):
    """Обработка ответов содержащихся в VIOLATION_CATEGORY
    """
    if call.data in get_data_list("VIOLATION_CATEGORY"):
        try:
            violation_data["violation_category"] = call.data
            await write_json_file(data=violation_data, name=violation_data["json_full_name"])

            await get_and_send_violation_category_data(call)

        except Exception as callback_err:
            logger.error(f"{repr(callback_err)}")
