import datetime

from app import MyBot
from apps.core.bot.data.report_data import headlines_data
from apps.core.bot.database.DataBase import DataBase
from apps.core.bot.messages.messages import Messages
from apps.core.bot.utils.generate_report.get_file_list import get_registration_json_file_list
from apps.core.bot.utils.json_worker.read_json_file import read_json_file
from loader import logger


async def get_act_headlines_data_values(chat_id, dataframe=None, act_date=None) -> dict:
    """ Формирование шапки акта - предписания

    :return: dict headlines_data
    """

    if not headlines_data:
        # TODO  get HSE database
        # ФИО выдавшего
        headlines_data['HSE'] = list(set(list(dataframe.name)))[0]

        headlines_data['HSE_name_short'] = 'Коршаков А.С.'
        # ФИО и должность выдавшего в родительном
        headlines_data['HSE_FUNC_RP'] = list(set(list(dataframe.name)))[0]
        # Email выдавшего
        headlines_data['HSE_email'] = 'as.korshakov@udokancopper.com'
        # Должность выдавшего
        headlines_data['HSE_function'] = list(set(list(dataframe.function)))[0]

        # TODO  get registry of acts
        headlines_data['act_number'] = 9999

        max_date = max(dataframe['created_at'])
        elimination_time_id = max(dataframe['elimination_time_id'])
        elimination_time: dict = DataBase().get_dict_data_from_table_from_id(
            table_name='core_eliminationtime',
            id=elimination_time_id)

        days_max = elimination_time['days']
        headlines_data['act_date'] = max_date
        headlines_data['act_max_date'] = datetime.datetime.strptime(act_date, '%d.%m.%Y') + datetime.timedelta(
            days=days_max)

        # Подрядчик
        general_contractor_id = list(set(list(dataframe.general_contractor_id)))[0]
        general_contractor_full_name: dict = DataBase().get_dict_data_from_table_from_id(
            table_name='core_generalcontractor',
            id=general_contractor_id)
        headlines_data['general_contractor_full_name'] = general_contractor_full_name['title']

        # TODO  update general_contractor table in DB
        # Ответственное лицо подрядчика
        headlines_data['contractor_representative'] = 'Ведущего специалиста по ОТ и ПБ ' \
                                                      'ООО «Ренейссанс Хэви Индастрис» Ковтуна С.Ю. '
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
    # date_then = datetime.datetime.now() - datetime.timedelta(days=1)
    # date_then = date_then.strftime("%d.%m.%Y")
    #
    # if headlines_data.get("work_shift").lower() == "дневная смена":
    #     headlines_data['work_shift'] = 'дневной смены'
    #     headlines_data['custom_date'] = f"{date_now}"
    #
    # else:
    #     headlines_data['work_shift'] = 'о ночной смене'
    #     headlines_data['custom_date'] = f"{date_then} - {date_now}"

    return headlines_data


async def set_act_header_values(worksheet, headlines_data_values=None, general_contractor=None):
    """Заполнение заголовка отчета
    
    :param general_contractor: 
    :param headlines_data_values: 
    :param worksheet:
    :return:
    """

    if not general_contractor:
        general_contractor = headlines_data_values.get('general_contractor', None)
    #     contractors = dataframe.general_contractor_id.tolist()
    #     contractors = list(set(list(contractors)))
    #     contractors_str = ''
    #     for item in contractors:
    #         if isinstance(item, float):
    #             continue
    #         if item and item != 'Подрядная организация':
    #             contractors_str = contractors_str + item + ', '
    #             headlines_data['contractors'] = contractors_str

    values = [
        {"coordinate": "B6", "value": f"Акт предписание №{headlines_data['act_number']} от "
                                      f"{str(headlines_data['act_date']).strftime('%d.%m.%Y')} г.",
         "row": "6", "column": "2"},

        {"coordinate": "B9", "value": f"{headlines_data['general_contractor_full_name']}",
         "row": "9", "column": "2"},

        {"coordinate": "B12", "value": f"{headlines_data['HSE_FUNC_RP']}",
         "row": "12", "column": "2"},

        {"coordinate": "B16", "value": f"{headlines_data['general_contractor_full_name']}",
         "row": "16", "column": "2"},

        {"coordinate": "B20", "value": f"{headlines_data['contractor_representative']}",
         "row": "20", "column": "2"},

        # {"coordinate": "B27", "value": f"тут наименование ПО",
        #  "row": "27", "column": "2"},

        {"coordinate": "G31", "value": f"{headlines_data['HSE_email']}",
         "row": "31", "column": "7"},

        {"coordinate": "G32", "value": f"{str(headlines_data['act_max_date']).strftime('%d.%m.%Y')}",
         "row": "32", "column": "7"},

        {"coordinate": "B43", "value": f"{headlines_data['HSE_function']}",
         "row": "43", "column": "2"},

        {"coordinate": "B43", "value": f"{headlines_data['HSE_name_short']}",
         "row": "43", "column": "11"},

        {"coordinate": "B46", "value": f"{str(headlines_data['act_date']).strftime('%d.%m.%Y')}",
         "row": "46", "column": "11"},

    ]

    for val in values:
        try:
            worksheet.cell(row=int(val['row']), column=int(val['column']), value=str(val['value']))
        except Exception as err:
            logger.error(f"set_user_values {repr(err)}")
            continue
