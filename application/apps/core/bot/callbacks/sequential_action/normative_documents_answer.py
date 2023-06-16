from loader import logger

logger.debug(f"{__name__} start import")
from aiogram import types
from apps.core.bot.callbacks.sequential_action.data_answer import (
    get_and_send_normative_documents_data,
    get_and_send_null_normative_documents_data)
from apps.core.bot.data.category import _PREFIX_ND, get_data_list
from apps.core.bot.reports.report_data import violation_data
from apps.core.bot.reports.report_data_preparation import \
    set_violation_atr_data
from apps.MyBot import MyBot

logger.debug(f"{__name__} finish import")


@MyBot.dp.callback_query_handler(
    lambda call: call.data in get_data_list("NORMATIVE_DOCUMENTS",
                                            category=violation_data.get("category", None),
                                            condition='short_title')
)
async def normative_documents_answer(call: types.CallbackQuery):
    """Обработка ответов содержащихся в NORMATIVE_DOCUMENTS
    """
    if call.data in get_data_list("NORMATIVE_DOCUMENTS",
                                  category=violation_data.get("category", None),
                                  condition='short_title'):

        if call.data == _PREFIX_ND + "0":
            await get_and_send_null_normative_documents_data(call)

            await set_violation_atr_data("normative_documents", 'Нет нужной записи')
            await set_violation_atr_data("normative_documents_normative", 'укажите НД')
            await set_violation_atr_data("normative_documents_procedure", 'укажите процедуру устранения по НД')
            return

        nd_data: list = []
        try:
            condition: dict = {
                "data": call.data,
                "category_in_db": "NORMATIVE_DOCUMENTS",
            }
            nd_data: list = get_data_list("NORMATIVE_DOCUMENTS",
                                          category=violation_data.get("category", None),
                                          condition=condition)
            if not nd_data:
                await set_violation_atr_data("normative_documents", call.data)

            nd_data = [item for item in nd_data if (isinstance(item, dict) and item.get("id", None))]

            await set_violation_atr_data("normative_documents", nd_data[0].get('title', None))
            await set_violation_atr_data("normative_documents_normative", nd_data[0].get('normative', None))
            await set_violation_atr_data("normative_documents_procedure", nd_data[0].get('procedure', None))

            await get_and_send_normative_documents_data(call)

        except Exception as callback_err:
            logger.error(f"{repr(callback_err)} {nd_data = }")
