import asyncio
from pprint import pprint

from aiogram import types

from app import MyBot

from apps.core.bot.data import board_config
from apps.core.bot.data.category import get_data_list
from apps.core.bot.data.report_data import violation_data
from apps.core.bot.keyboards.inline.build_castom_inlinekeyboard import build_inlinekeyboard
from apps.core.bot.utils.json_worker.writer_json_file import write_json_file
from apps.core.bot.messages.messages import Messages

from loader import logger

logger.debug("category_answer")


@MyBot.dp.callback_query_handler(lambda call: call.data in get_data_list("CATEGORY"))
async def category_answer(call: types.CallbackQuery):
    """Обработка ответов содержащихся в CATEGORY
    """
    if call.data in get_data_list("CATEGORY"):
        try:

            logger.debug(f"Выбрано: {call.data}")
            violation_data["category"] = call.data
            await call.message.answer(text=f"Выбрано: {call.data}")
            await write_json_file(data=violation_data, name=violation_data["json_full_name"])

            await call.message.edit_reply_markup()

            short_title = get_data_list("NORMATIVE_DOCUMENTS",
                                        category=violation_data["category"],
                                        condition='short_title'
                                        )
            data_list = get_data_list("NORMATIVE_DOCUMENTS",
                                      category=violation_data["category"],
                                      condition='data_list'
                                      )
            menu_level = board_config.menu_level = 1
            menu_list = board_config.menu_list = short_title

            zipped_list: list = list(zip(short_title, data_list))

            text = f'{Messages.Choose.normative_documents} \n\n' + \
                   ' \n\n'.join(str(item[0]) + " : " + str(item[1]) for item in zipped_list)

            reply_markup = await build_inlinekeyboard(some_list=menu_list, num_col=2, level=menu_level)
            await call.message.answer(text=text, reply_markup=reply_markup)

        except Exception as callback_err:
            logger.error(f"{repr(callback_err)}")


# async def test(call_data):
#     if call_data in get_data_list("CATEGORY"):
#         try:
#
#             # logger.debug(f"Выбрано: {call.data}")
#             # violation_data["category"] = call.data
#             # await call.message.answer(text=f"Выбрано: {call.data}")
#             # await write_json_file(data=violation_data, name=violation_data["json_full_name"])
#
#             # await call.message.edit_reply_markup()
#
#             short_title = get_data_list("NORMATIVE_DOCUMENTS",
#                                         category=call_data,
#                                         condition='short_title'
#                                         )
#             data_list = get_data_list("NORMATIVE_DOCUMENTS",
#                                       category=call_data,
#                                       condition='data_list'
#                                       )
#             # menu_level = board_config.menu_level = 1
#             # menu_list = board_config.menu_list = short_title
#             menu_list = short_title
#
#             ziped_list: list = zip(short_title, data_list)
#
#             text = f'{Messages.Choose.normative_documents} \n\n' + \
#                    ' \n\n'.join(str(item[0]) + " : " + str(item[1]) for item in ziped_list)
#             print(text)
#
#             reply_markup = await build_inlinekeyboard(some_list=menu_list, num_col=2, level=1)
#             # await call.message.answer(text=text, reply_markup=reply_markup)
#
#             pprint(reply_markup)
#
#         except Exception as callback_err:
#             logger.error(f"{repr(callback_err)}")
#
#
# if __name__ == "__main__":
#     asyncio.run(test(call_data='СИЗ'))
