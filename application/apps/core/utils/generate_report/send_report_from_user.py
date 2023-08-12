import datetime
import traceback

from apps.MyBot import bot_send_document
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

    caption = 'Отчет собран с помощью бота!'
    await bot_send_document(
        chat_id=chat_id, doc_path=full_report_path, caption=caption, fanc_name=await fanc_name()
    )


async def fanc_name():
    stack = traceback.extract_stack()
    return str(stack[-2][2])
