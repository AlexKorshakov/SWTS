from apps.core.utils.generate_report.generate_act_prescription.set_act_prescription_json import \
    set_act_prescription_json
from loader import logger

logger.debug(f"{__name__} start import")

from apps.core.bot.messages.messages import Messages
from apps.core.utils.goolgedrive_processor.GoogleDriveUtils.set_user_report_data_on_google_drive import \
    set_user_report_data_on_google_drive
from apps.MyBot import bot_send_message
from config.config import WRITE_DATA_ON_GOOGLE_DRIVE

logger.debug(f"{__name__} finish import")


async def set_report_data(chat_id: int, full_report_path: str):
    """Загрузка файла отчета на google drive

    :param chat_id: id чата
    :param full_report_path: полный путь до файла с данными
    """

    await set_user_report_data(chat_id=chat_id, full_report_path=full_report_path)
    await bot_send_message(chat_id=chat_id, text=Messages.Successfully.registration_completed)


async def set_user_report_data(chat_id: int, full_report_path: str):
    """Сoхранение данных отчета различными методами

    :param chat_id: id чата
    :param full_report_path: полный путь до файла с данными
    """
    if not full_report_path:
        await bot_send_message(chat_id=chat_id, text=Messages.Error.fill_report_path_not_found)
        logger.info(Messages.Error.fill_report_path_not_found)
        return

    if not WRITE_DATA_ON_GOOGLE_DRIVE:
        logger.info(f'{WRITE_DATA_ON_GOOGLE_DRIVE = } abort upload / download from Google Drive')
        return False

    if await set_user_report_data_on_google_drive(chat_id=chat_id, full_report_path=full_report_path):
        logger.info(Messages.Successfully.save_data_on_g_drive)


async def set_act_data_on_google_drive(chat_id: int, full_report_path: str):
    """Сoхранение данных отчета различными методами

    :param chat_id: id чата
    :param full_report_path: полный путь до файла с данными
    """

    if not WRITE_DATA_ON_GOOGLE_DRIVE:
        logger.info(f'{WRITE_DATA_ON_GOOGLE_DRIVE = } abort upload / download from Google Drive')
        return False

    if not full_report_path:
        await bot_send_message(chat_id=chat_id, text=Messages.Error.fill_report_path_not_found)
        logger.info(Messages.Error.fill_report_path_not_found)
        return

    if await set_user_report_data_on_google_drive(chat_id=chat_id, full_report_path=full_report_path):
        logger.info(Messages.Successfully.save_data_on_g_drive)


async def set_act_data_on_data_in_registry(
        hse_chat_id, act_dataframe, act_date, act_number, path_in_registry, constractor_id):
    """Сoхранение данных отчета различными методами"""

    act_prescription_json = await set_act_prescription_json(
        hse_chat_id=hse_chat_id, act_dataframe=act_dataframe, path_in_registry=path_in_registry,
        act_date=act_date, act_number=act_number, constractor_id=constractor_id)

    # await set_act_prescription_in_registry(act_prescription_json)

    await bot_send_message(chat_id=hse_chat_id, text=Messages.Successfully.registration_completed_in_registry)
