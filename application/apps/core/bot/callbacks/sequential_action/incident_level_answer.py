from aiogram import types

from app import MyBot
from apps.core.bot.callbacks.sequential_action.data_answer import get_and_send_incident_level_data
from apps.core.bot.data.category import get_data_list
from apps.core.bot.data.report_data import violation_data
from apps.core.bot.utils.json_worker.writer_json_file import write_json_file
from loader import logger

logger.debug("incident_level")


@MyBot.dp.callback_query_handler(lambda call: call.data in get_data_list("INCIDENT_LEVEL"))
async def incident_level(call: types.CallbackQuery):
    """Обработка ответов содержащихся в INCIDENT_LEVEL
    """
    if call.data in get_data_list("INCIDENT_LEVEL"):
        try:
            violation_data["incident_level"] = call.data
            await write_json_file(data=violation_data, name=violation_data["json_full_name"])

            await get_and_send_incident_level_data(call)

        except Exception as callback_err:
            logger.error(f"{repr(callback_err)}")
