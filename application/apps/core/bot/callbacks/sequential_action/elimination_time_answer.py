from aiogram import types

from app import MyBot
from apps.core.bot.callbacks.sequential_action.data_answer import get_and_send_elimination_time_data
from apps.core.bot.data.category import get_data_list
from apps.core.bot.data.report_data import violation_data
from apps.core.utils.json_worker.writer_json_file import write_json_file
from loader import logger

logger.debug("elimination_time_answer")


@MyBot.dp.callback_query_handler(lambda call: call.data in get_data_list("ELIMINATION_TIME"))
async def elimination_time_answer(call: types.CallbackQuery):
    """Обработка ответов содержащихся в ELIMINATION_TIME
    """
    if call.data in get_data_list("ELIMINATION_TIME"):
        try:
            violation_data["elimination_time"] = call.data
            await write_json_file(data=violation_data, name=violation_data["json_full_name"])

            await get_and_send_elimination_time_data(call)

        except Exception as callback_err:
            logger.error(f"{repr(callback_err)}")
