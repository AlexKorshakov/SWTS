from app import MyBot
from loader import logger

from apps.core.bot.messages.messages import Messages
from apps.core.bot.utils.generate_report.generator_report import create_report_from_other_method, create_mip_report
from apps.core.bot.utils.generate_report.get_data_report import get_data_report
from apps.core.bot.utils.generate_report.get_file_list import get_json_file_list
from apps.core.bot.utils.generate_report.get_report_path import get_full_report_name, get_full_mip_report_name
from apps.core.bot.utils.generate_report.send_report_from_user import send_report_from_user
from apps.core.bot.utils.set_user_report_data import set_report_data


async def create_and_send_report(chat_id):
    """Формирование и отправка отчета
    :param chat_id:
    :return:
    """

    file_list = await get_json_file_list(chat_id=chat_id)
    if not file_list:
        logger.warning(Messages.Error.file_list_not_found)
        await MyBot.bot.send_message(chat_id=chat_id, text=Messages.Error.file_list_not_found)

    dataframe = await get_data_report(chat_id=chat_id, file_list=file_list)
    if dataframe.empty:
        logger.warning(Messages.Error.dataframe_not_found)
        await MyBot.bot.send_message(chat_id=chat_id, text=Messages.Error.dataframe_not_found)

    full_report_path = await get_full_report_name(chat_id=chat_id)
    await create_report_from_other_method(chat_id=chat_id,
                                          dataframe=dataframe,
                                          full_report_path=full_report_path,
                                          file_list=file_list)

    await MyBot.bot.send_message(chat_id=chat_id, text=f'{Messages.Report.done} \n')

    await set_report_data(chat_id=chat_id, full_report_path=full_report_path)

    await send_report_from_user(chat_id=chat_id, full_report_path=full_report_path)

    return True


async def create_and_send_mip_report(chat_id) -> bool:
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

    await create_mip_report(chat_id=chat_id,
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
