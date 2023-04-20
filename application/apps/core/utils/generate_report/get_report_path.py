import datetime

from apps.core.database.db_utils import (db_get_data_dict_from_table_with_id,
                                         db_get_dict_userdata)

from apps.core.utils.secondary_functions.get_filepath import (
    create_file_path, get_report_full_filepath)
from loader import logger


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


async def get_full_daily_report_name(chat_id: int) -> str:
    """Получение полного пути к отчету
    :param chat_id:
    :return: полный путь к файлу с отчетом
    """
    now: str = (datetime.datetime.now()).strftime("%d.%m.%Y")
    userdata: dict = await db_get_dict_userdata(chat_id)
    location_id: int = int(userdata.get('hse_location', ''))

    location = await db_get_data_dict_from_table_with_id(
        table_name='core_location',
        post_id=location_id
    )
    location = location.get('title', '')

    try:
        report_full_name = f'ЛО-ОТ_ПБ_ПТ-{location} {now}.xlsx'
        report_path = await get_report_full_filepath(str(chat_id))
        await create_file_path(report_path)
        return report_path + report_full_name

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


async def get_full_stat_name(chat_id:int ):
    """Получение полного пути к отчету со статистикой

    :param chat_id:
    :return: полный путь к файлу с отчетом
    """
    now: str = (datetime.datetime.now()).strftime("%d.%m.%Y")
    userdata: dict = await db_get_dict_userdata(chat_id)
    location_id: int = int(userdata.get('hse_location', ''))

    location = await db_get_data_dict_from_table_with_id(
        table_name='core_location',
        post_id=location_id
    )
    location = location.get('title', '')

    try:
        report_full_name = f'СТАТ-ОТ_ПБ_ПТ-{location} {now}.xlsx'
        report_path = await get_report_full_filepath(str(chat_id))
        await create_file_path(report_path)
        return report_path + report_full_name

    except Exception as err:
        logger.error(f"get_report_path {repr(err)}")
        return ''
