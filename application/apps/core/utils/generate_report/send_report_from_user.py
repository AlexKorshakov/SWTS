import datetime
import traceback

from aiogram.types import ChatActions
from apps.core.utils.secondary_functions.get_filepath import (
    create_file_path, get_report_full_filepath)


async def send_report_from_user(chat_id, full_report_path=None):
    """Отправка пользователю сообщения с готовым отчетом
    """

    if not full_report_path:
        report_name = f'МИП Отчет за {(datetime.datetime.now()).strftime("%d.%m.%Y")}.xlsx'
        report_path = await get_report_full_filepath(str(chat_id))
        await create_file_path(report_path)
        full_report_path = report_path + report_name

    await MyBot.bot.send_chat_action(chat_id=chat_id, action=ChatActions.UPLOAD_DOCUMENT)
    await asyncio.sleep(2)  # скачиваем файл и отправляем его пользователю


async def fanc_name():
    stack = traceback.extract_stack()
    return str(stack[-2][2])
