from aiogram import types

from app import MyBot
from apps.core.bot.data import board_config
from apps.core.bot.data.category import get_data_list
from apps.core.bot.data.report_data import violation_data
from apps.core.bot.keyboards.inline.build_castom_inlinekeyboard import build_inlinekeyboard
from apps.core.bot.messages.messages import Messages
from apps.core.bot.utils.json_worker.writer_json_file import write_json_file
from loader import logger
logger.debug("main_location_answer")


@MyBot.dp.callback_query_handler(lambda call: call.data in get_data_list("MAIN_LOCATIONS"))
async def main_location_answer(call: types.CallbackQuery):
    """Обработка ответов содержащихся в MAIN_LOCATIONS
    """
    for i in get_data_list("MAIN_LOCATIONS"):
        try:
            if call.data == i:
                logger.debug(f"Выбрано: {i}")
                violation_data["main_location"] = i
                await call.message.answer(text=f"Выбрано: {i}")
                await write_json_file(data=violation_data, name=violation_data["json_full_name"])

                await call.message.edit_reply_markup()
                short_title = get_data_list("SUB_LOCATIONS",
                                            category=violation_data["main_location"],
                                            condition='short_title'
                                            )
                data_list = get_data_list("SUB_LOCATIONS",
                                          category=violation_data["main_location"],
                                          condition='data_list'
                                          )
                menu_level = board_config.menu_level = 1
                menu_list = board_config.menu_list = short_title

                zipped_list: list = list(zip(short_title, data_list))

                text = f'{Messages.Choose.sub_location} \n\n' + \
                       ' \n\n'.join(str(item[0]) + " : " + str(item[1]) for item in zipped_list)

                reply_markup = await build_inlinekeyboard(some_list=menu_list, num_col=2, level=menu_level)
                await call.message.answer(text=text, reply_markup=reply_markup)

                break

        except Exception as callback_err:
            logger.error(f"{repr(callback_err)}")
