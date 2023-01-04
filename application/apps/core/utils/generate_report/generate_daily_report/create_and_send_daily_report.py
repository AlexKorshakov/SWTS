from apps.MyBot import MyBot
from apps.core.bot.messages.messages import Messages
from apps.core.utils.data_recording_processor.set_user_report_data import set_report_data
from apps.core.utils.generate_report.generate_daily_report.create_daily_report import create_daily_report
from apps.core.utils.generate_report.get_data_report import get_data_report
from apps.core.utils.generate_report.get_file_list import get_json_file_list
from apps.core.utils.generate_report.get_report_path import get_full_mip_report_name
from apps.core.utils.generate_report.send_report_from_user import send_report_from_user
from loader import logger


async def create_and_send_daily_report(chat_id) -> bool:
    """Формирование и отправка отчета

    :param chat_id:
    :return:
    """

    full_mip_report_path: str = await get_full_mip_report_name(chat_id=chat_id)

    file_list = await get_json_file_list(chat_id=chat_id)
    if not file_list:
        logger.error(Messages.Error.file_list_not_found)
        await MyBot.bot.send_message(chat_id=chat_id, text=Messages.Error.file_list_not_found)
        return False

    dataframe = await get_data_report(chat_id=chat_id, file_list=file_list)
    if dataframe.empty:
        logger.error(Messages.Error.dataframe_not_found)
        await MyBot.bot.send_message(chat_id=chat_id, text=Messages.Error.dataframe_not_found)
        return False

    await create_daily_report(chat_id=chat_id,
                              dataframe=dataframe,
                              full_mip_report_path=full_mip_report_path,
                              violation_data=file_list
                              )

    await MyBot.bot.send_message(chat_id=chat_id, text=f'{Messages.Report.done} \n')

    await set_report_data(chat_id=chat_id, full_report_path=full_mip_report_path)

    await send_report_from_user(chat_id=chat_id, full_report_path=full_mip_report_path)

    full_mip_report_path = full_mip_report_path.replace(".xlsx", ".pdf")

    await send_report_from_user(chat_id=chat_id, full_report_path=full_mip_report_path)

    return True