from aiogram import types

from app import MyBot

from apps.core.bot.data.category import get_data_list
from apps.core.bot.data.report_data import violation_data
from apps.core.bot.states import AnswerUserState
from apps.core.bot.utils.json_worker.writer_json_file import write_json_file
from apps.core.bot.messages.messages import Messages

from loader import logger

logger.debug("elimination_time_answer")


@MyBot.dp.callback_query_handler(lambda call: call.data in get_data_list("ELIMINATION_TIME"))
async def elimination_time_answer(call: types.CallbackQuery):
    """Обработка ответов содержащихся в ELIMINATION_TIME
    """
    for i in get_data_list("ELIMINATION_TIME"):
        try:
            if call.data == i:
                logger.debug(f"Выбрано: {i}")
                violation_data["elimination_time"] = i
                await write_json_file(data=violation_data, name=violation_data["json_full_name"])

                await call.message.edit_reply_markup()
                await call.message.answer(Messages.Enter.description_violation)
                await AnswerUserState.description.set()

                break

        except Exception as callback_err:
            logger.error(f"{repr(callback_err)}")
