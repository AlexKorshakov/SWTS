from loader import logger

logger.debug(f"{__name__} start import")
from aiogram import types
from apps.core.bot.callbacks.sequential_action.data_answer import \
    get_and_send_main_locations_data
from apps.core.bot.data.category import get_data_list
from apps.core.bot.reports.report_data_preparation import \
    set_violation_atr_data
from apps.MyBot import MyBot

logger.debug(f"{__name__} finish import")


@MyBot.dp.callback_query_handler(lambda call: call.data in get_data_list("MAIN_LOCATIONS", condition='short_title'))
async def main_location_answer(call: types.CallbackQuery):
    """Обработка ответов содержащихся в MAIN_LOCATIONS
    """
    if call.data in get_data_list("MAIN_LOCATIONS", condition='short_title'):
        try:
            await set_violation_atr_data("main_location", call.data)

            await get_and_send_main_locations_data(call)

        except Exception as callback_err:
            logger.error(f"{repr(callback_err)}")

