from loader import logger

logger.debug(f"{__name__} start import")
from aiogram import types
from aiogram.dispatcher import FSMContext
from apps.core.bot.reports.report_data import ViolationData
from apps.core.database.db_utils import db_get_data_list
from apps.core.database.query_constructor import QueryConstructor
from apps.core.bot.callbacks.sequential_action.data_answer import get_and_send_main_locations_data
from apps.core.bot.callbacks.sequential_action.category import get_data_list
from apps.core.bot.reports.report_data_preparation import set_violation_atr_data
from apps.MyBot import MyBot

logger.debug(f"{__name__} finish import")


@MyBot.dp.callback_query_handler(lambda call: call.data in get_data_list("MAIN_LOCATIONS", condition='short_title'),
                                 state=ViolationData.all_states)
async def main_location_answer(call: types.CallbackQuery, state: FSMContext):
    """Обработка ответов содержащихся в MAIN_LOCATIONS
    """
    await set_violation_atr_data("main_location", art_val=call.data, state=state)
    try:

        kwargs: dict = {
            "action": 'SELECT', "subject": 'id',
            "conditions": {
                "short_title": f"{call.data}",
            }
        }
        query: str = await QueryConstructor(table_name='core_mainlocation', **kwargs).prepare_data()

        datas_query: list = await db_get_data_list(query=query)
        main_category_id = datas_query[0][0] if datas_query else None
        await set_violation_atr_data("main_location_id", main_category_id, state=state)

        await get_and_send_main_locations_data(call, state=state)

    except Exception as callback_err:
        logger.error(f"{repr(callback_err)}")
