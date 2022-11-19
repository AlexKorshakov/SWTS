from aiogram import types

from app import MyBot

from apps.core.bot.data import board_config
from apps.core.bot.data.category import get_data_list
from apps.core.bot.data.report_data import violation_data
from apps.core.bot.database.DataBase import DataBase, CATEGORY_ID_TRANSFORM
from apps.core.bot.keyboards.inline.build_castom_inlinekeyboard import build_inlinekeyboard, \
    add_previous_paragraph_button
from apps.core.bot.utils.json_worker.writer_json_file import write_json_file
from apps.core.bot.messages.messages import Messages

from loader import logger

logger.debug("general_contractors_answer")


@MyBot.dp.callback_query_handler(lambda call: call.data in get_data_list("GENERAL_CONTRACTORS"))
async def general_contractors_answer(call: types.CallbackQuery):
    """Обработка ответов содержащихся в GENERAL_CONTRACTORS
    """

    for i_name in get_data_list("GENERAL_CONTRACTORS"):
        try:
            if call.data == i_name:
                logger.info(f"Выбрано: {i_name}")

                value = DataBase().get_full_title(table_name=CATEGORY_ID_TRANSFORM['general_contractor']['table'],
                                                  short_title=i_name)

                violation_data["general_contractor"] = value
                await call.message.answer(text=f"Выбрано: {i_name}")
                await write_json_file(data=violation_data, name=violation_data["json_full_name"])

                await call.message.edit_reply_markup()
                menu_level = board_config.menu_level = 1
                menu_list = board_config.menu_list = get_data_list("INCIDENT_LEVEL")
                count_col = board_config.count_col = 1

                reply_markup = await build_inlinekeyboard(some_list=menu_list, num_col=count_col, level=menu_level)
                reply_markup = await add_previous_paragraph_button(
                    reply_markup=reply_markup,
                    previous_level='general_contractors'
                )

                await call.message.answer(text=Messages.Choose.incident_level, reply_markup=reply_markup)
                break

        except Exception as callback_err:
            logger.error(f"{repr(callback_err)}")
