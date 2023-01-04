import datetime

from apps.MyBot import MyBot
from apps.core.utils.generate_report.get_file_list import get_registration_json_file_list
from loader import logger

from apps.core.bot.messages.messages import Messages
from apps.core.utils.json_worker.read_json_file import read_json_file
from apps.core.utils.secondary_functions.get_filepath import create_file_path, get_report_full_filepath


async def get_full_report_name(chat_id: int) -> str:
    """Получение полного пути к отчету
    :rtype: str
    :param chat_id:
    :return: полный путь к файлу с отчетом
    """
    try:
        report_full_name: str = f'МИП Отчет за {(datetime.datetime.now()).strftime("%d.%m.%Y")}.xlsx'

        report_path = await get_report_full_filepath(str(chat_id))
        await create_file_path(report_path)
        full_report_path: str = report_path + report_full_name
        return full_report_path

    except Exception as err:
        logger.error(f"get_report_path {repr(err)}")
        return ''


async def get_full_mip_report_name(chat_id: int) -> str:
    """Получение полного пути к отчету
    :param chat_id:
    :return: полный путь к файлу с отчетом
    """

    registration_file_list = await get_registration_json_file_list(chat_id=chat_id)
    if not registration_file_list:
        logger.warning(Messages.Error.registration_file_list_not_found)
        await MyBot.bot.send_message(chat_id=chat_id, text=Messages.Error.file_list_not_found)
        return ''

    registration_data = await read_json_file(registration_file_list)
    location_name = registration_data.get('name_location')

    if location_name is None:
        logger.warning(Messages.Error.location_name_not_found)
        await MyBot.bot.send_message(chat_id=chat_id, text=Messages.Error.location_name_not_found)
        location_name = ''

    try:
        report_full_name = f'ЛО-МИП-УОТиПБ НС-{location_name} {(datetime.datetime.now()).strftime("%d.%m.%Y")}.xlsx'
        report_path = await get_report_full_filepath(str(chat_id))
        await create_file_path(report_path)
        full_report_path: str = report_path + report_full_name
        return full_report_path

    except Exception as err:
        logger.error(f"get_report_path {repr(err)}")
        return ''


async def get_and_create_full_act_prescription_name(chat_id: int, param: dict) -> str:
    """Формирование и получение полного имение пути к акту

    :param param:
    :param chat_id:
    :return:
    """
    if not param:
        return ''

    act_number = param.get('act_number', None)
    if not act_number:
        act_number = (datetime.datetime.now()).strftime("%d.%m.%Y")

    act_date = param.get('act_date', None)
    if not act_date:
        act_date = (datetime.datetime.now()).strftime("%d.%m.%Y")

    short_title = param.get('short_title', None)
    if not short_title:
        short_title = ''

    main_location = param.get('main_location', None)
    if not main_location:
        main_location = ''

    try:
        report_full_name = f'Акт-предписание № {act_number} от {act_date} {short_title} {main_location}.xlsx'
        report_path = await get_report_full_filepath(str(chat_id), actual_date=act_date)
        await create_file_path(report_path)
        full_report_path: str = report_path + report_full_name

        return full_report_path

    except Exception as err:
        logger.error(f"get_report_path {repr(err)}")
        return ''
