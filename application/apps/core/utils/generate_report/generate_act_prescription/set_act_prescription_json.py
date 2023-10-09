from __future__ import annotations

import asyncio
import datetime

from pandas import DataFrame
from apps.core.database.db_utils import db_get_data_dict_from_table_with_id, db_get_table_headers, db_get_data_list, \
    db_get_dict_userdata
from apps.core.utils.json_worker.writer_json_file import write_json_file
from apps.core.utils.secondary_functions.get_filepath import get_report_full_name


async def set_act_prescription_json(hse_chat_id: str | int, act_dataframe: DataFrame, act_number: str | int,
                                    path_in_registry: str, constractor_id: str | int, act_date: str):
    """Формирование json-файла со ВСЕМИ данными акта - предписания

    :return:
    """
    act_prescription_json = None
    act_data_dict: dict = {}
    item_list = []

    unique_id = act_dataframe.id.unique().tolist()

    v_index = 0
    for v_index, v_id, in enumerate(unique_id, start=1):
        item_v_df = act_dataframe.copy(deep=True)
        item_df = item_v_df.loc[item_v_df['id'] == v_id]

        if item_v_df.empty:
            continue

        item_data_dict = {}
        for (key, value) in item_df.items():
            if value.values.dtype == 'int64':
                value = value.values[0].item()
                item_data_dict[key] = value
            else:
                item_data_dict[key] = value.get(v_index - 1, None)

        item_list.append(
            {item_data_dict['id']: item_data_dict}
        )

    hse_userdata: dict = await db_get_dict_userdata(hse_chat_id)
    hse_organization_id = hse_userdata.get('hse_organization')

    hse_organization_dict: dict = await db_get_data_dict_from_table_with_id(
        table_name='core_generalcontractor', post_id=hse_organization_id)

    contractor: dict = await db_get_data_dict_from_table_with_id(
        table_name='core_generalcontractor', post_id=constractor_id)

    act_data_dict['violations'] = [
        {'violations_items': item_list},
        {'violations_index': v_index},
    ]

    act_data_dict['contractor'] = contractor
    act_data_dict['hse_userdata'] = hse_userdata
    act_data_dict['hse_organization'] = hse_organization_dict

    # TODO Дополнить заголовками и пр.

    contractor_data: dict = await get_general_constractor_data(
        constractor_id=constractor_id, type_constractor='general'
    )
    if not contractor_data:
        return ''

    short_title = contractor_data.get('short_title')

    report_full_name = f'Акт-предписание № {act_number} от {act_date} {short_title}.json'
    full_patch_to_act_prescription_json = await get_report_full_name(path_in_registry, report_full_name)

    await write_json_file(data=act_data_dict, name=full_patch_to_act_prescription_json)

    return act_prescription_json


async def get_clean_headers(table_name: str) -> list:
    """Получение заголовков таблицы по имени table_name

    :param table_name: str - имя таблицы для получения заголовков
    :return: list[str] or []
    """

    if not table_name:
        return []

    headers: list = await db_get_table_headers(table_name=table_name)
    clean_headers: list = [item[1] for item in headers]
    # logger.debug(clean_headers)

    return clean_headers


async def get_general_constractor_data(constractor_id: int, type_constractor: str) -> dict:
    """Получение данных из таблицы `core_generalcontractor` по constractor_id

    :return:
    """
    contractor: dict = {}

    if type_constractor == 'general':
        contractor = await db_get_data_dict_from_table_with_id(
            table_name='core_generalcontractor',
            post_id=constractor_id)

    if type_constractor == 'sub':
        contractor = await db_get_data_dict_from_table_with_id(
            table_name='core_subcontractor',
            post_id=constractor_id)

    if not contractor:
        return {}

    return contractor


async def get_act_dataframe(chat_id, act_period: list, constractor_id, headers):
    """Получение dataframe с данными акта - предписания

    :return:
    """

    # TODO заменить на вызов конструктора QueryConstructor
    table_name: str = 'core_violations'
    query: str = f'SELECT * ' \
                 f'FROM {table_name} ' \
                 f"WHERE `act_number` = 1151 " \
                 f"AND `general_contractor_id` = {constractor_id} " \
                 f"AND `created_at` BETWEEN date('{await format_data_db(act_period[0])}') " \
                 f"AND date('{await format_data_db(act_period[1])}') " \
                 f"AND `user_id` = {chat_id}"

    act_dataframe: DataFrame = await create_lite_dataframe_from_query(
        chat_id=chat_id, query=query, clean_headers=headers
    )

    return act_dataframe


async def format_data_db(date_item: str):
    """ Форматирование даты в формат даты БВ
    """
    return datetime.datetime.strptime(date_item, "%d.%m.%Y").strftime("%Y-%m-%d")


async def create_lite_dataframe_from_query(chat_id: int, query: str, clean_headers: list) -> DataFrame:
    """Формирование dataframe из запроса query и заголовков clean_headers

    :param chat_id: id  пользователя
    :param clean_headers: заголовки таблицы для формирования dataframe
    :param query: запрос в базу данных
    :return:
    """

    item_datas_query: list = await db_get_data_list(query=query)
    report_dataframe: DataFrame = await create_lite_dataframe(
        chat_id=chat_id, data_list=item_datas_query, header_list=clean_headers
    )

    # if report_dataframe.empty:
    #     logger.error(f'{Messages.Error.dataframe_is_empty}  \n{chat_id = }  \n{query = }  \n{item_datas_query = }')
    #     await bot_send_message(chat_id=chat_id, text=Messages.Error.dataframe_is_empty)

    return report_dataframe


async def create_lite_dataframe(chat_id, data_list: list, header_list: list):
    """Создание dataframe

    :param chat_id:
    :param header_list: список с заголовками
    :param data_list: список с данными
    """
    try:
        dataframe: DataFrame = DataFrame(data_list, columns=header_list)
        return dataframe

    except Exception as err:
        # logger.error(F"create_dataframe {repr(err)}")
        return None


async def test():
    chat_id = '373084462'
    constractor_id = 2

    now = datetime.datetime.now()
    previous = now - datetime.timedelta(days=1)
    query_act_date_period: list = [previous.strftime("%d.%m.%Y"), now.strftime("%d.%m.%Y"), ]

    clean_headers: list = await get_clean_headers(table_name='core_violations')

    act_dataframe: DataFrame = await get_act_dataframe(
        chat_id=chat_id, act_period=query_act_date_period, constractor_id=constractor_id, headers=clean_headers
    )
    if act_dataframe.empty:
        return

    hse_chat_id = '373084462'
    act_number = '1151'
    path_in_registry = 'C:\\Users\\KDeusEx\\PycharmProjects\\SWTS\\application\\media\\registry\\' \
                       'ООО Удоканская Медь\\2023\\04\\Акт-предписание № 1151 от 30.04.2023 ООО РХИ'
    act_date = '24.04.2023'

    await set_act_prescription_json(hse_chat_id, act_dataframe, act_number,
                                    path_in_registry, constractor_id, act_date)


if __name__ == '__main__':
    asyncio.run(test())
