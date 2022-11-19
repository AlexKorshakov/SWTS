from aiogram import types

from app import MyBot
from apps.core.bot.callbacks.sequential_action.data_answer import get_and_send_null_sub_locations_data, \
    get_and_send_sub_locations_data
from apps.core.bot.data.category import get_data_list, _PREFIX_POZ
from apps.core.bot.data.report_data import violation_data
from apps.core.bot.utils.json_worker.writer_json_file import write_json_file
from loader import logger

logger.debug("sub_location_answer")


@MyBot.dp.callback_query_handler(
    lambda call: call.data in get_data_list("SUB_LOCATIONS",
                                            category=violation_data["main_location"],
                                            condition='short_title'
                                            )
)
async def sub_location_answer(call: types.CallbackQuery):
    """Обработка ответов содержащихся в NORMATIVE_DOCUMENTS
    """
    if call.data in get_data_list("SUB_LOCATIONS",
                                  category=violation_data["main_location"],
                                  condition='short_title'):

        if call.data == _PREFIX_POZ + "0":
            await get_and_send_null_sub_locations_data(call)

        try:
            condition: dict = {
                "data": call.data,
                "category_in_db": "SUB_LOCATIONS",
            }
            sub_loc = get_data_list("SUB_LOCATIONS",
                                    category=violation_data["main_location"],
                                    condition=condition)
            if not sub_loc:
                violation_data["sub_location"] = call.data

            violation_data["sub_location"] = sub_loc[0].get('title', None)
            await write_json_file(data=violation_data, name=violation_data["json_full_name"])
            await get_and_send_sub_locations_data(call)

        except Exception as callback_err:
            logger.error(f"{repr(callback_err)}")
