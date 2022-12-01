import asyncio
import datetime
from pprint import pprint

from apps.core.bot.database.DataBase import DataBase
from apps.core.bot.reports.report_data import headlines_data
from apps.core.utils.reports_processor.report_worker_utils import get_clean_headers
from loader import logger


async def get_act_headlines_data_values(chat_id, dataframe=None, act_date=None, act_number=None) -> dict:
    """ Формирование данных для формирования шапки акта - предписания

    :return: dict headlines_data
    """

    if not headlines_data:
        # TODO  get HSE database
        pprint(f'{chat_id = }')

        table_name: str = 'core_violations'
        clean_headers: list = await get_clean_headers(table_name=table_name)

        query: str = f'SELECT * FROM `core_hseuser` WHERE `hse_telegram_id` == {chat_id}'
        datas_query_list: list = DataBase().get_data_list(query=query)

        item_dict: dict = dict((header, item_value) for header, item_value in zip(clean_headers, datas_query_list[0]))

        hse_id = item_dict.get('id', None)
        pprint(f'{hse_id = }')

        if not hse_id:
            logger.error(f'hse_id is {hse_id}')
            return

        # hse_id = list(set(list(dataframe.hse_id)))[0]
        # pprint(f'{dataframe.hse_id = }')
        pprint(f'{hse_id = }')

        hse_user: dict = DataBase().get_dict_data_from_table_from_id(
            table_name='core_hseuser',
            id=hse_id)

        pprint(f'{hse_user = }')

        # ФИО выдавшего
        # headlines_data['HSE'] = list(set(list(dataframe.name)))[0]
        headlines_data['HSE'] = hse_user.get('hse_full_name', None)

        # ФИО сокращенно выдавшего
        # headlines_data['HSE_name_short'] = 'Коршаков А.С.'
        headlines_data['HSE_name_short'] = hse_user.get('hse_short_name', None)

        # ФИО и должность выдавшего в родительном
        # headlines_data['HSE_full_name_dative'] = list(set(list(dataframe.name)))[0]
        headlines_data['HSE_full_name_dative'] = hse_user.get('hse_full_name_dative', None)

        # Email выдавшего
        # headlines_data['HSE_email'] = 'as.korshakov@udokancopper.com'
        headlines_data['HSE_email'] = hse_user.get('hse_contact_main_email', None)

        # Должность выдавшего
        # headlines_data['HSE_function'] = list(set(list(dataframe.function)))[0]
        headlines_data['HSE_function'] = hse_user.get('hse_function', None)
        headlines_data['HSE_function_dative'] = hse_user.get('hse_function_dative', None)

        # Отдел выдавшего
        # headlines_data['hse_department'] = list(set(list(dataframe.function)))[0]
        headlines_data['hse_department'] = hse_user.get('hse_department', None)
        headlines_data['hse_department_dative'] = hse_user.get('hse_department_dative', None)

        headlines_data['act_number'] = act_number if act_number else 00000

        elimination_time_id = max(dataframe['elimination_time_id'])
        elimination_time: dict = DataBase().get_dict_data_from_table_from_id(
            table_name='core_eliminationtime',
            id=elimination_time_id)

        max_date = max(dataframe['created_at'])
        days_max = elimination_time['days']
        headlines_data['act_date'] = datetime.datetime.strptime(max_date, '%Y-%m-%d').strftime('%d.%m.%Y')
        headlines_data['act_max_date'] = (datetime.datetime.strptime(act_date, '%d.%m.%Y') + datetime.timedelta(
            days=days_max)).strftime('%d.%m.%Y')

        # Подрядчик
        general_contractor_id = list(set(list(dataframe.general_contractor_id)))[0]
        general_contractor_full_name: dict = DataBase().get_dict_data_from_table_from_id(
            table_name='core_generalcontractor',
            id=general_contractor_id)
        headlines_data['general_contractor_full_name'] = general_contractor_full_name['title']

        # TODO  update general_contractor table in DB
        # Ответственное лицо подрядчика
        headlines_data['contractor_representative'] = ' '
        # Проект
        main_location_id_list: list = list(set(list(dataframe.main_location_id)))
        item_dict: dict = {}
        for main_location_id in main_location_id_list:
            main_location_name: dict = DataBase().get_dict_data_from_table_from_id(
                table_name='core_mainlocation',
                id=main_location_id)
            item_dict[main_location_id] = main_location_name

        headlines_data['main_location'] = item_dict

        # # Вид обхода
        # headlines_data['linear_bypass'] = 'Первичный'
        # # Дата
        # headlines_data['date_linear_bypass'] = ''
        # # Представитель подрядчика
        # headlines_data['contractor_representative'] = be_away
        # # Представитель субподрядчика
        # headlines_data['subcontractor_representative'] = be_away

    headlines_data["day"] = (datetime.datetime.now()).strftime("%d")
    headlines_data["year"] = (datetime.datetime.now()).strftime("%Y")

    # # if not user_data:
    # registration_file_list = await get_registration_json_file_list(chat_id=chat_id)
    # if not registration_file_list:
    #     logger.warning(Messages.Error.registration_file_list_not_found)
    #     await MyBot.bot.send_message(chat_id=chat_id, text=Messages.Error.file_list_not_found)
    #     return
    #
    # registration_data = await read_json_file(registration_file_list)
    #
    # headlines_data['function'] = registration_data.get("function")
    # headlines_data['name'] = registration_data.get("name")
    # headlines_data['name_location'] = registration_data.get("name_location")
    # headlines_data['phone_number'] = registration_data.get("phone_number")
    # headlines_data['work_shift'] = registration_data.get("work_shift")
    #
    # date_now = datetime.datetime.now().strftime("%d.%m.%Y")
    # date_before_now = datetime.datetime.now() - datetime.timedelta(days=1)
    # date_before_now = date_before_now.strftime("%d.%m.%Y")

    return headlines_data


async def set_act_header_values(worksheet, headlines_data=None):
    """Заполнение заголовка отчета
    
    :param headlines_data:
    :param worksheet:
    :return:
    """
    # TODO  get HSE database
    values: list = [
        {"coordinate": "B6",
         "value": f"Акт предписание № {headlines_data.get('act_number', 'act_number')} от "
                  f"{headlines_data.get('act_date', 'act_date')} г.",
         "row": "6",
         "column": "2"},

        {"coordinate": "B9",
         "value": f"{headlines_data.get('general_contractor_full_name', 'general_contractor_full_name')}",
         "row": "9",
         "column": "2"},

        {"coordinate": "B12",
         "value": f"{headlines_data.get('HSE_function_dative', 'HSE_function_dative')} "
                  f"{headlines_data.get('hse_department_dative', 'hse_department_dative')} "
                  f"{headlines_data.get('HSE_full_name_dative', 'HSE_full_name_dative')}",
         "row": "12",
         "column": "2"},

        {"coordinate": "B16",
         "value": f"{headlines_data.get('general_contractor_full_name', 'general_contractor_full_name')}",
         "row": "16",
         "column": "2"},

        {"coordinate": "B20",
         "value": f"{headlines_data.get('contractor_representative', 'contractor_representative')}",
         "row": "20",
         "column": "2"},
    ]

    for val in values:
        try:
            worksheet.cell(row=int(val['row']), column=int(val['column']), value=str(val['value']))
        except Exception as err:
            logger.error(f"set_user_values {repr(err)}")
            continue


async def set_act_footer_footer_values(worksheet, row_number):
    """Установка значений футера акта

    :param worksheet:
    :param row_number:
    :return:
    """
    # TODO  get HSE database
    row_value = 28 + row_number

    values: list = [
        {"coordinate": "G31",
         "value": f"{headlines_data['HSE_email']}",
         "row": f"{31 - 28 + row_value}",
         "column": "7"},

        {"coordinate": "G32",
         "value": f"{(headlines_data['act_max_date'])}",
         "row": f"{32 - 28 + row_value}",
         "column": "7"},

        {"coordinate": "B43",
         "value": f"{headlines_data['HSE_function']} {headlines_data['hse_department_dative']}",
         "row": f"{43 - 28 + row_value}",
         "column": "2"},

        {"coordinate": "B43",
         "value": f"{headlines_data['HSE_name_short']}",
         "row": f"{43 - 28 + row_value}",
         "column": "11"},

        {"coordinate": "B46",
         "value": f"{headlines_data['act_date']}",
         "row": f"{46 - 28 + row_value}",
         "column": "11"},
    ]

    for val in values:
        try:
            worksheet.cell(row=int(val['row']), column=int(val['column']), value=str(val['value']))
        except Exception as err:
            logger.error(f"set_user_values {repr(err)}")
            continue


async def test():
    chat_id = 862629360
    await get_act_headlines_data_values(chat_id)


if __name__ == "__main__":
    asyncio.run(test())
