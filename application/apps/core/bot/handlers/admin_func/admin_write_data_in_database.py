from __future__ import annotations

from datetime import date, datetime
from sqlite3 import OperationalError

from apps.core.database.ViolationsDataBase import DataBaseViolations
from apps.core.database.db_utils import (db_add_user,
                                         db_get_clean_headers,
                                         db_get_table_headers)
from loader import logger


async def write_data_in_database(*, user_data_to_db: dict, admin_id: int | str) -> bool:
    """Поиск записи по file_id в database

    :param user_data_to_db:
    :param admin_id:
    :return: True or False
    """
    if not user_data_to_db.get('hse_telegram_id'):
        logger.error(f"Error get file_id for violation_data: {user_data_to_db}")
        return False

    # if await db_check_record_existence(user_telegram_id=user_data_to_db.get('user_telegram_id')):
    #     return False

    result, user_data_to_db = await prepare_violation_data(user_data_dict=user_data_to_db, admin_id=admin_id)
    if not result:
        return False

    user_data_to_db: dict = await normalize_violation_data(user_data_to_db)
    user_data_to_db: dict = await check_violation_data(user_data_to_db)

    try:

        if not await db_add_user(hseuser_data=user_data_to_db):
            logger.error(
                f"Error add_user by {admin_id} user_telegram_id = {user_data_to_db.get('hse_telegram_id')} in DB!!")
            return False

        return True

    except OperationalError as err:
        logger.error(f"Error add_violation in DataBase() : {repr(err)}")
        return False

    except Exception as err:
        logger.error(f"Error add_violation in DataBase() : {repr(err)}")
        return False


async def db_check_record_existence(user_telegram_id: int) -> bool:
    """Проверка наличия записи в БД

    :param user_telegram_id: int - id записи
    :return: bool is_exists
    """
    is_exists: bool = await DataBaseViolations().user_exists(user_telegram_id=user_telegram_id)
    if is_exists:
        return True

    return False


async def normalize_violation_data(user_data: dict = None) -> dict:
    """

    :return:
    """
    clean_headers: list = await db_get_clean_headers(table_name='core_hseuser')
    keys_to_remove = [item for item in list(user_data.keys()) if item not in clean_headers]

    for key in keys_to_remove:

        try:
            del user_data[key]
            logger.info(f'{key = } remove from user_data')

        except (KeyError, RuntimeError) as err:
            logger.error(f'{key = } err remove from user_data err {repr(err)}')
            continue

        except Exception as err:
            logger.error(f'{key = } Exception remove from user_data err {repr(err)}')
            continue

    return user_data


async def check_violation_data(user_data: dict = None) -> dict:
    """

    :return:
    """
    not_null_values_headers: list = [row[1] for row in await db_get_table_headers('core_hseuser') if row[3] != 0]

    for key, value in user_data.items():
        if key not in not_null_values_headers:
            continue

        if user_data.get(key) is None:
            logger.info(f'{key = } {value = } from user_data')

    return user_data


async def prepare_violation_data(user_data_dict: dict, admin_id: int | str = None) -> (bool, dict):
    """

    :param user_data_dict:
    :param admin_id:
    :return:
    """

    user_telegram_id = user_data_dict.get('user_telegram_id', None)

    if not user_telegram_id:
        logger.error('not found user_telegram_id!!!')
        return False, user_data_dict

    user_data_dict.update({'user_telegram_id': user_data_dict})

    title = user_data_dict.get('title', None)
    user_data_dict.update({'title': title})

    hse_telegram_id = user_data_dict.get('hse_telegram_id', None)
    user_data_dict.update({'hse_telegram_id': hse_telegram_id})

    hse_tab_number = user_data_dict.get('hse_tab_number', None)
    user_data_dict.update({'hse_tab_number': hse_tab_number})

    hse_full_name = user_data_dict.get('hse_full_name', None)
    user_data_dict.update({'hse_full_name': hse_full_name})

    hse_full_name_dative = user_data_dict.get('hse_full_name_dative', None)
    user_data_dict.update({'hse_full_name_dative': hse_full_name_dative})

    hse_short_name = user_data_dict.get('hse_short_name', None)
    user_data_dict.update({'hse_short_name': hse_short_name})

    hse_full_name_telegram = user_data_dict.get('hse_full_name_telegram', None)
    user_data_dict.update({'hse_full_name_telegram': hse_full_name_telegram})

    hse_function = user_data_dict.get('hse_function', None)
    user_data_dict.update({'hse_function': hse_function})

    hse_function_dative = user_data_dict.get('hse_function_dative', None)
    user_data_dict.update({'hse_function_dative': hse_function_dative})

    hse_department = user_data_dict.get('hse_department', None)
    user_data_dict.update({'hse_department': hse_department})

    hse_department_dative = user_data_dict.get('hse_department_dative', None)
    user_data_dict.update({'hse_department_dative': hse_department_dative})

    hse_language_code = user_data_dict.get('hse_language_code', None)
    user_data_dict.update({'hse_language_code': hse_language_code})

    hse_is_work = user_data_dict.get('hse_is_work', None)
    user_data_dict.update({'hse_is_work': hse_is_work})

    hse_status = user_data_dict.get('hse_status', None)
    user_data_dict.update({'hse_status': hse_status})

    hse_status_comment = user_data_dict.get('hse_status_comment', None)
    user_data_dict.update({'hse_status_comment': hse_status_comment})

    hse_organization = user_data_dict.get('hse_organization', None)
    user_data_dict.update({'hse_organization': hse_organization})

    hse_role_is_author = user_data_dict.get('hse_role_is_author', None)
    user_data_dict.update({'hse_role_is_author': hse_role_is_author})

    hse_role_is_developer = user_data_dict.get('hse_role_is_developer', None)
    user_data_dict.update({'hse_role_is_developer': hse_role_is_developer})

    hse_role_is_admin = user_data_dict.get('hse_role_is_admin', None)
    user_data_dict.update({'hse_role_is_admin': hse_role_is_admin})

    hse_role_is_coordinating_person = user_data_dict.get('hse_role_is_coordinating_person', None)
    user_data_dict.update({'hse_role_is_coordinating_person': hse_role_is_coordinating_person})

    hse_role_is_super_user = user_data_dict.get('hse_role_is_super_user', None)
    user_data_dict.update({'hse_role_is_super_user': hse_role_is_super_user})

    hse_role_is_user = user_data_dict.get('hse_role_is_user', None)
    user_data_dict.update({'hse_role_is_user': hse_role_is_user})

    hse_role_is_subcontractor = user_data_dict.get('hse_role_is_subcontractor', None)
    user_data_dict.update({'hse_role_is_subcontractor': hse_role_is_subcontractor})

    hse_role_receive_notifications = user_data_dict.get('hse_role_receive_notifications', None)
    user_data_dict.update({'hse_role_receive_notifications': hse_role_receive_notifications})

    hse_role_is_user_bagration = user_data_dict.get('hse_role_is_user_bagration', None)
    user_data_dict.update({'hse_role_is_user_bagration': hse_role_is_user_bagration})

    hse_role_is_emploee_tc = user_data_dict.get('hse_role_is_emploee_tc', None)
    user_data_dict.update({'hse_role_is_emploee_tc': hse_role_is_emploee_tc})

    hse_location = user_data_dict.get('hse_location', None)
    user_data_dict.update({'hse_location': hse_location})

    hse_work_shift = user_data_dict.get('hse_work_shift', None)
    user_data_dict.update({'hse_work_shift': hse_work_shift})

    hse_contact_main_phone_number = user_data_dict.get('hse_contact_main_phone_number', None)
    user_data_dict.update({'hse_contact_main_phone_number': hse_contact_main_phone_number})

    hse_contact_second_phone_number = user_data_dict.get('hse_contact_second_phone_number', None)
    user_data_dict.update({'hse_contact_second_phone_number': hse_contact_second_phone_number})

    hse_contact_main_email = user_data_dict.get('hse_contact_main_email', None)
    user_data_dict.update({'hse_contact_main_email': hse_contact_main_email})

    hse_contact_second_email = user_data_dict.get('hse_contact_second_email', None)
    user_data_dict.update({'hse_contact_second_email': hse_contact_second_email})

    hse_folder_parent_id = user_data_dict.get('hse_folder_parent_id', None)
    user_data_dict.update({'hse_folder_parent_id': hse_folder_parent_id})

    hse_folder_json_id = user_data_dict.get('hse_folder_json_id', None)
    user_data_dict.update({'hse_folder_json_id': hse_folder_json_id})

    hse_folder_report_id = user_data_dict.get('hse_folder_report_id', None)
    user_data_dict.update({'hse_folder_report_id': hse_folder_report_id})

    hse_folder_photo_id = user_data_dict.get('hse_folder_photo_id', None)
    user_data_dict.update({'hse_folder_photo_id': hse_folder_photo_id})

    day = await get_day_message()
    month = await get_month_message()
    year = await get_year_message()
    created_at = '.'.join([day, month, year])
    user_data_dict.update({'created_at': created_at})

    updated_at = created_at
    user_data_dict.update({'updated_at': updated_at})

    update_information: str = f'update by {admin_id = } hse_telegram_id {hse_telegram_id} at {created_at} ' \
                              f'for first entry in current registry'
    user_data_dict.update({'update_information': update_information})

    return True, user_data_dict


async def str_to_datetime(date_str: str) -> date:
    """Преобразование str даты в datetime

    :param
    """

    current_date: datetime = datetime.now()
    try:
        if isinstance(date_str, str):
            current_date: date = datetime.strptime(date_str, "%d.%m.%Y").date()
    except ValueError as err:
        logger.error(f"{repr(err)}")

    return current_date


async def get_day_message(current_date: datetime | str = None) -> str:
    """Обработчик сообщений с фото
    Получение номер str дня из сообщения в формате dd
    """

    current_date: date = await str_to_datetime(current_date)

    if not current_date:
        current_date: datetime = datetime.now()
    return str("0" + str(current_date.day) if current_date.day < 10 else str(current_date.day))


async def get_month_message(current_date: datetime | str = None) -> str:
    """Получение номер str месяца из сообщения в формате mm
    """
    current_date: date = await str_to_datetime(current_date)

    if not current_date:
        current_date: datetime = datetime.now()
    return str("0" + str(current_date.month) if int(current_date.month) < 10 else str(current_date.month))


async def get_year_message(current_date: datetime | str = None) -> str:
    """Обработчик сообщений с фото
    Получение полного пути файла
    """
    current_date: date = await str_to_datetime(current_date)

    if not current_date:
        current_date: datetime = datetime.now()

    return str(current_date.year)
