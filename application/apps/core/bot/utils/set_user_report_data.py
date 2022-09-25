from app import MyBot
from loader import logger

from apps.core.bot.messages.messages import Messages
from apps.core.bot.utils.goolgedrive.GoogleDriveUtils.set_user_report_data_on_google_drive import \
    set_user_report_data_on_google_drive


async def set_report_data(chat_id: int, full_report_path: str):
    """Загрузка файла отчета на google drive

    :param chat_id: id чата
    :param full_report_path: полный путь до файла с данными
    """

    await set_user_report_data(chat_id=chat_id, full_report_path=full_report_path)
    await MyBot.dp.bot.send_message(chat_id=chat_id, text=Messages.Successfully.registration_completed)


async def set_user_report_data(chat_id: int, full_report_path: str):
    """Сoхранение данных отчета различными методами

    :param chat_id: id чата
    :param full_report_path: полный путь до файла с данными
    """
    if not full_report_path:
        await MyBot.dp.bot.send_message(chat_id=chat_id, text=Messages.Error.fill_report_path_not_found)
        logger.info(Messages.Error.fill_report_path_not_found)
        return

    if await set_user_report_data_on_google_drive(chat_id=chat_id, full_report_path=full_report_path):
        logger.info(Messages.Successfully.save_data_on_g_drive)


async def set_act_data_on_google_drive(chat_id: int, full_report_path: str):
    """Сoхранение данных отчета различными методами

    :param chat_id: id чата
    :param full_report_path: полный путь до файла с данными
    """
    if not full_report_path:
        await MyBot.dp.bot.send_message(chat_id=chat_id, text=Messages.Error.fill_report_path_not_found)
        logger.info(Messages.Error.fill_report_path_not_found)
        return

    if await set_user_report_data_on_google_drive(chat_id=chat_id, full_report_path=full_report_path):
        logger.info(Messages.Successfully.save_data_on_g_drive)
