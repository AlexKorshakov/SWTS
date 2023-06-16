from loader import logger

logger.debug(f"{__name__} start import")
from aiogram import types
from apps.core.bot.data import board_config
from apps.core.bot.data.category import get_data_list
from apps.core.bot.keyboards.inline.build_castom_inlinekeyboard import (
    add_previous_paragraph_button, build_inlinekeyboard)
from apps.core.bot.messages.messages import Messages
from apps.core.bot.reports.report_data import violation_data
from apps.core.database.db_utils import db_get_full_title
from apps.core.database.transformation_category import CATEGORY_ID_TRANSFORM
from apps.core.utils.json_worker.writer_json_file import write_json_file
from apps.MyBot import MyBot, bot_send_message

logger.debug(f"{__name__} finish import")


@MyBot.dp.callback_query_handler(lambda call: call.data in get_data_list("GENERAL_CONTRACTORS"))
async def general_contractors_answer(call: types.CallbackQuery):
    """Обработка ответов содержащихся в GENERAL_CONTRACTORS
    """
    chat_id = call.message.chat.id
    for i_name in get_data_list("GENERAL_CONTRACTORS"):
        try:
            if call.data == i_name:
                logger.info(f"{chat_id = }  Выбрано: {i_name}")

                value = await db_get_full_title(table_name=CATEGORY_ID_TRANSFORM['general_contractor']['table'],
                                                short_title=i_name)

                violation_data["general_contractor"] = value
                await bot_send_message(chat_id=chat_id, text=f"Выбрано: {i_name}")
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

                await bot_send_message(chat_id=chat_id, text=Messages.Choose.incident_level, reply_markup=reply_markup)
                break

        except Exception as callback_err:
            logger.error(f"{repr(callback_err)}")
