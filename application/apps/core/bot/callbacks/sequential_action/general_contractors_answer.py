from aiogram import types

from app import MyBot

from apps.core.bot.data import board_config
from apps.core.bot.data.category import get_names_from_json
from apps.core.bot.data.report_data import violation_data
from apps.core.bot.keyboards.inline.build_castom_inlinekeyboard import build_inlinekeyboard
from apps.core.bot.utils.json_worker.writer_json_file import write_json_file
from apps.core.bot.messages.messages import Messages

from loader import logger
logger.debug("general_contractors_answer")

@MyBot.dp.callback_query_handler(lambda call: call.data in get_names_from_json("GENERAL_CONTRACTORS"))
async def general_contractors_answer(call: types.CallbackQuery):
    """Обработка ответов содержащихся в GENERAL_CONTRACTORS
    """
    for i in get_names_from_json("GENERAL_CONTRACTORS"):
        try:
            if call.data == i:
                logger.debug(f"Выбрано: {i}")
                violation_data["general_contractor"] = i
                await call.message.answer(text=f"Выбрано: {i}")
                await write_json_file(data=violation_data, name=violation_data["json_full_name"])

                await call.message.edit_reply_markup()
                menu_level = board_config.menu_level = 1
                menu_list = board_config.menu_list = get_names_from_json("INCIDENT_LEVEL")

                reply_markup = await build_inlinekeyboard(some_list=menu_list, num_col=1, level=menu_level)
                await call.message.answer(text=Messages.Choose.incident_level, reply_markup=reply_markup)
                break

        except Exception as callback_err:
            logger.error(f"{repr(callback_err)}")
