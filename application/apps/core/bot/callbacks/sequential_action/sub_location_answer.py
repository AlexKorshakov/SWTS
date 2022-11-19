from aiogram import types

from app import MyBot

from apps.core.bot.data import board_config
from apps.core.bot.data.category import get_data_list, _PREFIX_POZ
from apps.core.bot.data.report_data import violation_data
from apps.core.bot.keyboards.inline.build_castom_inlinekeyboard import build_inlinekeyboard
from apps.core.bot.utils.json_worker.writer_json_file import write_json_file
from apps.core.bot.messages.messages import Messages

from loader import logger

logger.debug("sub_location_answer")


@MyBot.dp.callback_query_handler(
    lambda call: call.data in get_data_list("SUB_LOCATIONS",
                                            category=violation_data["main_location"],
                                            condition='short_title')
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
            logger.debug(f"Выбрано: {call.data}")
            await call.message.answer(text=f"Выбрано: {call.data}")

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

            await call.message.edit_reply_markup()
            menu_level = board_config.menu_level = 1
            menu_list = board_config.menu_list = get_data_list("MAIN_CATEGORY")

            reply_markup = await build_inlinekeyboard(some_list=menu_list, num_col=1, level=menu_level)
            await call.message.answer(text=Messages.Choose.violation_category, reply_markup=reply_markup)

        except Exception as callback_err:
            logger.error(f"{repr(callback_err)}")
