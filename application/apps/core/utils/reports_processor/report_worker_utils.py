from datetime import datetime
from openpyxl.utils import dataframe

from pandas import DataFrame

from app import MyBot
from apps.core.bot.database.DataBase import DataBase
from apps.core.bot.messages.messages import Messages
from apps.core.utils.generate_report.create_dataframe import create_lite_dataframe

from loader import logger


async def get_clear_list_value(chat_id: int, query: str, clean_headers: list) -> list[dict]:
    """Получение очищенных данных

    :return: clear_list : list
    """

    datas_query: list = DataBase().get_data_list(query=query)

    if not datas_query:
        logger.info(Messages.Error.data_not_found)
        await MyBot.bot.send_message(chat_id=chat_id, text=Messages.Error.data_not_found)
        return []

    clear_list_value: list = []
    for items_value in datas_query:
        item_dict: dict = dict((header, item_value) for header, item_value in zip(clean_headers, items_value))
        clear_list_value.append(item_dict)

    return clear_list_value


async def get_general_constractor_list(clear_list_value: list) -> list:
    """Получение списка get_general_constractor_list

    """
    general_constractor_list = [item_value.get('general_contractor_id') for item_value in clear_list_value]
    general_constractor_list = list(set(general_constractor_list))

    return general_constractor_list


async def get_sub_locations_ids_list(clear_list_value: list) -> list:
    """Получение списка get_general_constractor_list

    """
    sub_locations_ids_list = [item_value.get('sub_location_id') for item_value in clear_list_value]
    sub_locations_ids_list = list(set(sub_locations_ids_list))

    return sub_locations_ids_list


async def get_general_constractor_data(constractor_id: int, type_constractor: str) -> dict:
    """Получение данных из таблицы `core_generalcontractor` по constractor_id

    :return:
    """
    contractor: dict = {}

    if type_constractor == 'general':
        contractor = DataBase().get_dict_data_from_table_from_id(
            table_name='core_generalcontractor',
            id=constractor_id)

    if type_constractor == 'sub':
        contractor = DataBase().get_dict_data_from_table_from_id(
            table_name='core_subcontractor',
            id=constractor_id)

    if not contractor:
        return {}

    return contractor


async def get_clean_headers(table_name: str) -> list:
    """Получение заголовков таблицы

    :param
    """

    if not table_name:
        return []

    headers = DataBase().get_table_headers(table_name=table_name)
    clean_headers: list = [item[1] for item in headers]
    return clean_headers


async def create_lite_dataframe_from_query(chat_id: int, query: str, clean_headers: list) -> dataframe:
    """

    :return:
    """

    item_datas_query: list = DataBase().get_data_list(query=query)

    report_dataframe: DataFrame = await create_lite_dataframe(data_list=item_datas_query, header_list=clean_headers)

    if report_dataframe.empty:
        logger.error(Messages.Error.dataframe_not_found)
        await MyBot.bot.send_message(chat_id=chat_id, text=Messages.Error.dataframe_not_found)

    return report_dataframe


async def get_query(type_query: str, table_name: str, query_act_date: str = None, value_id: int = None,
                    **kvargs) -> str:
    """

    """
    query = ''
    if type_query == 'general_contractor_id':
        query: str = f'SELECT * ' \
                     f'FROM {table_name} ' \
                     f"WHERE (`created_at` = date('{query_act_date}') " \
                     f"AND (`act_number` = '' or `act_number` is NULL ) " \
                     f"AND `general_contractor_id` = {value_id})"

    if type_query == 'sub_location_id':
        query: str = f'SELECT * ' \
                     f'FROM {table_name} ' \
                     f"WHERE (`created_at` = date('{query_act_date}') " \
                     f"AND (`act_number` = '' or `act_number` is NULL ) " \
                     f"AND `sub_location_id` = {value_id})"

    if type_query == 'query_act':
        if isinstance(query_act_date, list):
            query: str = f'SELECT * ' \
                         f'FROM {table_name} ' \
                         f"WHERE (`act_number` = '' or `act_number` is NULL ) " \
                         f"AND `created_at` BETWEEN date('{await format_data_db(query_act_date[0])}') " \
                         f"AND date('{await format_data_db(query_act_date[1])}')"

        if isinstance(query_act_date, str):
            query: str = f'SELECT * ' \
                         f'FROM {table_name} ' \
                         f"WHERE (`created_at` = date('{query_act_date}') " \
                         f"AND (`act_number` = '' or `act_number` is NULL ))"

    return query


async def format_data_db(date_item: str):
    """ Форматирование даты в формат даты БВ
    """
    return datetime.strptime(date_item, "%d.%m.%Y").strftime("%Y-%m-%d")