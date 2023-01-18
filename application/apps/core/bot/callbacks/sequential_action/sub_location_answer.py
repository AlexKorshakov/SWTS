from aiogram import types

from apps.MyBot import MyBot
from apps.core.bot.callbacks.sequential_action.data_answer import get_and_send_null_sub_locations_data, \
    get_and_send_sub_locations_data
from apps.core.bot.data.category import get_data_list, _PREFIX_POZ
from apps.core.bot.reports.report_data import violation_data
from apps.core.bot.reports.report_data_preparation import set_violation_atr_data
from loader import logger

logger.debug("sub_location_answer")


@MyBot.dp.callback_query_handler(
    lambda call: call.data in get_data_list("SUB_LOCATIONS",
                                            category=violation_data.get("main_location", None),
                                            condition='short_title'
                                            )
)
async def sub_location_answer(call: types.CallbackQuery):
    """Обработка ответов содержащихся в NORMATIVE_DOCUMENTS
    """
    if call.data in get_data_list("SUB_LOCATIONS",
                                  category=violation_data.get("main_location", None),
                                  condition='short_title'):

        if call.data == _PREFIX_POZ + "0":
            await get_and_send_null_sub_locations_data(call)

        try:
            condition: dict = {
                "data": call.data,
                "category_in_db": "SUB_LOCATIONS",
            }
            sub_loc = get_data_list("SUB_LOCATIONS",
                                    category=violation_data.get("main_location", None),
                                    condition=condition)
            if not sub_loc:
                await set_violation_atr_data("sub_location", call.data)

            await set_violation_atr_data("sub_location", sub_loc[0].get('title', None))
            await get_and_send_sub_locations_data(call)

        except Exception as callback_err:
            logger.error(f"{repr(callback_err)}")
