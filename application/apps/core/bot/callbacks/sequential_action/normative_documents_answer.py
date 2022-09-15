from aiogram import types

from app import MyBot

from apps.core.bot.data import board_config
from apps.core.bot.data.category import get_data_list
from apps.core.bot.data.report_data import violation_data
from apps.core.bot.database.DataBase import DataBase
from apps.core.bot.keyboards.inline.build_castom_inlinekeyboard import build_inlinekeyboard
from apps.core.bot.utils.json_worker.writer_json_file import write_json_file
from apps.core.bot.messages.messages import Messages

from loader import logger

logger.debug("normative_documents_answer")


@MyBot.dp.callback_query_handler(
    lambda call: call.data in get_data_list("NORMATIVE_DOCUMENTS",
                                            category=violation_data["category"],
                                            condition='short_title')
)
async def category_answer(call: types.CallbackQuery):
    """Обработка ответов содержащихся в NORMATIVE_DOCUMENTS
    """
    if call.data in get_data_list("NORMATIVE_DOCUMENTS",
                                  category=violation_data["category"],
                                  condition='short_title'):
        try:
            logger.debug(f"Выбрано: {call.data}")
            await call.message.answer(text=f"Выбрано: {call.data}")

            condition: dict = {
                "data": call.data,
                "category_in_db": "NORMATIVE_DOCUMENTS",
            }

            nd_data = get_data_list("NORMATIVE_DOCUMENTS",
                                    category=violation_data["category"],
                                    condition=condition)
            if not nd_data:
                violation_data["normative_documents"] = call.data

            violation_data["normative_documents"] = nd_data[0].get('title', None)
            violation_data["normative_documents_normative"] = nd_data[0].get('normative', None)
            violation_data["normative_documents_procedure"] = nd_data[0].get('procedure', None)

            await write_json_file(data=violation_data, name=violation_data["json_full_name"])

            await call.message.edit_reply_markup()
            menu_level = board_config.menu_level = 1
            menu_list = board_config.menu_list = get_data_list("VIOLATION_CATEGORY")

            reply_markup = await build_inlinekeyboard(some_list=menu_list, num_col=1, level=menu_level)
            await call.message.answer(text=Messages.Choose.violation_category, reply_markup=reply_markup)

        except Exception as callback_err:
            logger.error(f"{repr(callback_err)}")
