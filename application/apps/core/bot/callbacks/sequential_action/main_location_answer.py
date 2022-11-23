from aiogram import types

from app import MyBot
from apps.core.bot.callbacks.sequential_action.data_answer import get_and_send_main_locations_data
from apps.core.bot.data.category import get_data_list
from apps.core.bot.data.report_data import violation_data
from apps.core.utils.json_worker.writer_json_file import write_json_file
from loader import logger

logger.debug("main_location_answer")


@MyBot.dp.callback_query_handler(lambda call: call.data in get_data_list("MAIN_LOCATIONS", condition='short_title'))
async def main_location_answer(call: types.CallbackQuery):
    """Обработка ответов содержащихся в MAIN_LOCATIONS
    """
    if call.data in get_data_list("MAIN_LOCATIONS", condition='short_title'):
        try:
            violation_data["main_location"] = call.data
            await write_json_file(data=violation_data, name=violation_data["json_full_name"])

            await get_and_send_main_locations_data(call)

        except Exception as callback_err:
            logger.error(f"{repr(callback_err)}")
