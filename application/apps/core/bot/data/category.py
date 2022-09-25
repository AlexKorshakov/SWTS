import inspect
import json
import os.path
from json import JSONDecodeError
from typing import Union

from apps.core.bot.database.DataBase import DataBase
from loader import logger

filename = inspect.getframeinfo(inspect.currentframe()).filename
PATH = os.path.dirname(os.path.abspath(filename))

MAIN_CATEGORY: list = [
    "Охрана труда",
    "Промышленная безопасность",
    "Пожарная безопасность",
    "Экология",
    "БДД",
    "ГО и ЧС",
]

CATEGORY: list = [
    "Документы ОТ и ПБ",
    "Обучение, аттестация/квалификация",
    "СИЗ",
    "Механизмы и оборудование",
    "ТС/Спецтехника",
    "Знаки безопасности/ограждения",
    "Земляные работы",
    "Электробезопасность",
    "Бетонные работы",
    "ГПМ",
    "Замкнутые пространства",
    "Ручные инструменты",
    "Работы на высоте",
    "Огневые работы",
    "Оборудование под давлением",
    "Пожарная безопасность",
    "Первая помощь",
    "Химические, биологические факторы",
    "Санитарные требования",
    "Складирование",
    "Безопасные проходы",
    "Отходы",
    "Освещение",
    "Другое"
]

VIOLATION_CATEGORY: list = [
    "Опасные действия*",
    "RWC (Ограниченный рабочий случай)",
    "Опасная ситуация*",
    "NearMiss (Происшествие без последствий)",
    "FAT (со смертельным исходом)",
    "LTI (травма с врем. потерей трудоспособности)",
    "Лёгкий НС",
    "RTA (дорожно-транспортное происшествие)",
    "Тяжелый и групповой НС"
]

GENERAL_CONTRACTORS: list = [
    "Строй-Монтаж 2002(?)",
    "МИП - Строй 1(?)",
    "СиАрСиСи Рус(?)",
    "ГорИнжПроект(?)",
    "Прочее(?)"
]

ACT_REQUIRED: list = [
    "Требуется*",
    "Не требуется",
]

INCIDENT_LEVEL: list = [
    'Без последствий',
    'Лёгкий',
    'Серьезный',
    'Катастрофический',
]

ELIMINATION_TIME: list = [
    "Постоянно",
    "Немедленно",
    "1 день",
    "3 дня",
    "5 дней",
    "7 дней",
    "10 дней",
    "15 дней",
    "21 день",
    "30 дней"
]

SENT_TO: list = [
    "arsutinaa@mosinzhproekt.ru",
    "lozhkov.rd@mosinzhproekt.ru"
]

CORRECT_COMMANDS_LIST: list = [
    'Состав комиссии',
    'Корректировать значения',
    'Удалить Полностью'
]

REGISTRATION_DATA_LIST: list = [
    "ФИО",
    "Должность",
    "Место работы",
    "Смена",
    "Телефон"
]

HEADLINES_DATA_LIST: list = [
    "Руководитель строительства",
    "Инженер СК",
    "Подрядчик",
    "Субподрядчик",
    "Вид обхода",
    "Представитель подрядчика",
    "Представитель субподрядчика"
]

VIOLATIONS_DATA_LIST: list = [
    "Описание нарушения",
    "Комментарий к нарушению",
    "Основное направление",
    "Количество дней на устранение",
    "Степень опасности ситуации",
    "Требуется ли оформление акта?",
    "Подрядная организация",
    "Категория нарушения",
    "Уровень происшествия"
]

ADMIN_MENU_LIST: list = [
    'Показать всех пользователей',
    'Оповещение'
]

ALL_CATEGORY: dict = {
    'MAIN_CATEGORY': MAIN_CATEGORY,
    'CATEGORY': CATEGORY,
    'VIOLATION_CATEGORY': VIOLATION_CATEGORY,
    'GENERAL_CONTRACTORS': GENERAL_CONTRACTORS,
    'ACT_REQUIRED': ACT_REQUIRED,
    'INCIDENT_LEVEL': INCIDENT_LEVEL,
    'ELIMINATION_TIME': ELIMINATION_TIME,
    'SENT_TO': SENT_TO,
    'CORRECT_COMMANDS_LIST': CORRECT_COMMANDS_LIST,
    'REGISTRATION_DATA_LIST': REGISTRATION_DATA_LIST,
    'HEADLINES_DATA_LIST': HEADLINES_DATA_LIST,
    'VIOLATIONS_DATA_LIST': VIOLATIONS_DATA_LIST,
    'ADMIN_MENU_LIST': ADMIN_MENU_LIST,
}

_PREFIX_ND: str = 'nrm_doc_'
_PREFIX_POZ: str = 'nrm_poz_'


def convert_category_name(category_in_db: str) -> str:
    """

    :param category_in_db:
    :return:
    """
    all_category_in_db: dict = {
        'MAIN_CATEGORY': 'core_maincategory',
        'CATEGORY': 'core_category',
        'VIOLATION_CATEGORY': 'core_violationcategory',
        'GENERAL_CONTRACTORS': 'core_generalcontractor',
        'ACT_REQUIRED': 'core_actrequired',
        'INCIDENT_LEVEL': 'core_incidentlevel',
        'ELIMINATION_TIME': 'core_eliminationtime',
        'LOCATIONS': 'core_location',
        'NORMATIVE_DOCUMENTS': 'core_normativedocuments',
        'MAIN_LOCATIONS': 'core_mainlocation',
        'SUB_LOCATIONS': 'core_sublocation',

    }

    db_table_name = all_category_in_db[category_in_db]
    return db_table_name


def add_null_value_to_ziped_list(zip_list: list) -> list:
    """
    
    :param zip_list: 
    :return: 
    """

    zip_list.append(
        {
            'title': 'Нет нужной записи'
        }
    )

    return zip_list


def add_null_value_to_list(zip_list: list, condition: str, db_table_name: str) -> list:
    """

    :param condition:
    :param zip_list:
    :return:
    """

    if condition == 'data_list':
        zip_list.append(f'Нет нужной записи')

    if condition == 'short_title':
        if db_table_name == 'core_normativedocuments':
            zip_list.append(_PREFIX_ND + '0')

        if db_table_name == 'core_sublocation':
            zip_list.append(_PREFIX_POZ + '0')

    return zip_list


def get_category_data_list_whits_single_condition(db_table_name: str, item_id: int, single_condition: str) -> list:
    """ Получение данных если single_condition

    :param single_condition:
    :param item_id:
    :param db_table_name:
    :return:
    """

    if db_table_name == 'core_sublocation':
        query: str = f'SELECT * FROM {db_table_name} WHERE `main_location_id` == {item_id}'

    if db_table_name == 'core_normativedocuments':
        query: str = f'SELECT * FROM {db_table_name} WHERE `category_id` == {item_id}'

    datas_query: list = DataBase().get_data_list(query=query)

    if not datas_query:
        return []
    if not isinstance(datas_query, list):
        return []

    if single_condition == 'short_title':

        if db_table_name == 'core_sublocation':
            clean_datas_query: list = [_PREFIX_POZ + str(item[0]) for item in datas_query]

        if db_table_name == 'core_normativedocuments':
            clean_datas_query: list = [_PREFIX_ND + str(item[0]) for item in datas_query]

        return clean_datas_query

    if single_condition == 'data_list':
        clean_datas_query: list = [item[2] for item in datas_query]
        return clean_datas_query


def get_category_data_list_whits_dict_condition(db_table_name, dict_condition) -> list:
    """ Получение данных если single_condition

    :return:
    """

    if not isinstance(dict_condition, dict):
        return []

    if not dict_condition.get("data", None):
        return []

    if db_table_name == 'core_sublocation':
        item_id = dict_condition.get("data", None).replace(_PREFIX_POZ, '')

    if db_table_name == 'core_normativedocuments':
        item_id = dict_condition.get("data", None).replace(_PREFIX_ND, '')

    query: str = f'SELECT * FROM {db_table_name} WHERE `id` == {item_id}'
    datas_query: list = DataBase().get_data_list(query=query)

    if not datas_query:
        return []
    if not isinstance(datas_query, list):
        return []

    table_headers = DataBase().get_table_headers(table_name=db_table_name)
    headers = [item[1] for item in table_headers]
    item_datas = list(datas_query[0])

    data_dict: dict = {}
    for header, item_data in zip(headers, item_datas):
        data_dict[header] = item_data

    condition = dict_condition.get("condition", None)
    if not condition:
        return [data_dict]


def get_category_data_list_whits_condition(db_table_name: str, category, condition: Union[str, dict]) -> list:
    """Получение

    :param category:
    :param db_table_name:
    :type condition: Union[str, dict]

    """
    main_table_name: str = 'core_violations'

    if db_table_name == 'core_normativedocuments':
        main_table_name = 'core_category'

    if db_table_name == 'core_sublocation':
        main_table_name = 'core_mainlocation'

    category_id = DataBase().get_id(table=main_table_name, entry=category)
    if not category_id:
        return []

    if isinstance(condition, str):
        datas_from_bd: list = get_category_data_list_whits_single_condition(db_table_name=db_table_name,
                                                                            item_id=category_id,
                                                                            single_condition=condition)
        datas_from_bd = add_null_value_to_list(datas_from_bd, condition, db_table_name)
        return datas_from_bd

    if isinstance(condition, dict):
        datas_from_bd = get_category_data_list_whits_dict_condition(db_table_name=db_table_name,
                                                                    dict_condition=condition)
        datas_from_bd = add_null_value_to_ziped_list(datas_from_bd)
        return datas_from_bd
    return []


def get_data_from_db(db_table_name: str) -> list:
    """Получение
    """

    query: str = f'SELECT * FROM {db_table_name}'
    datas_query: list = DataBase().get_data_list(query=query)
    headers: list = [item[1] for item in DataBase().get_table_headers(table_name=db_table_name)]

    if not isinstance(datas_query, list):
        return []

    if 'short_title' in headers:
        data_list = [data[2] for data in datas_query]
        return data_list

    if datas_query:
        logger.debug(f'retrieved data from database: {datas_query}')
        data_list = [data[1] for data in datas_query]
        return data_list

    return []


def get_data_list(category_in_db: str = None, category: str = None, condition: Union[str, dict] = None) -> list:
    """ Функция получения данных из базы данных. При отсутствии данных поиск в json.
    При наличии condition - формирование данных согласно  condition

    :param category:
    :param category_in_db:
    :type condition: Union[str, dict]
    :return: data_list or [ ]
    """

    db_table_name = convert_category_name(category_in_db)
    if not db_table_name:
        return []

    if category and condition:
        clean_datas_query = get_category_data_list_whits_condition(
            db_table_name=db_table_name, category=category,
            condition=condition
        )
        logger.debug(f'get_category_data_list from db with condition: {clean_datas_query}')
        return clean_datas_query

    data_list = get_data_from_db(db_table_name=db_table_name)

    if data_list:
        logger.debug(f'get data from db: {data_list}')
        return data_list

    if not data_list:
        data_list = get_data_from_json(name=category_in_db)
        logger.debug(f'retrieved data from json:')
        return data_list


def get_data_from_json(name):
    if not name:
        return []

    try:
        with open(PATH + "\\" + name + ".json", "r", encoding="UTF-8") as read_file:
            list_value = json.loads(read_file.read())
            if not list_value:

                if name not in [key for key, value in ALL_CATEGORY.items()]:
                    return []

                return ALL_CATEGORY[name]

            return list_value

    except (FileNotFoundError, JSONDecodeError) as err:
        logger.error(f" {name} {repr(err)}")
        return []

# if __name__ == "__main__":
# for item in ALL_CATEGORY_IN_DB:
#     datas = get_data_list(category_name=item)
#
#     for i in datas:
#         if len(i.encode('utf-8')) > 62:
#             print(f" {i} : {len(i.encode('utf-8'))}")
#
#             while int(len(i.encode('utf-8'))) > 62:
#                 i = i[:-1]
#                 print(f" {i} : {len(i.encode('utf-8'))}")
#
#             i = i[:-2] + '...'
#             print(f" {i} : {len(i.encode('utf-8'))}")
#
# pprint(datas)
#
# data_list: list = get_data_list(category_name='NORMATIVE_DOCUMENTS', category='Промышленная безопасность_')
#
# pprint(data_list)
# category = 'ТК ГОК'
#
# dict_condition: dict = {
#     # "condition": "short_title",
#     "data": _PREFIX_ND + '1',
#     "category_in_db": "SUB_LOCATIONS",
#     # "category_name": violation_data["category"]
# }
#
# menu_list: list = get_data_list("SUB_LOCATIONS",
#                                 category=category,
#                                 condition='short_title'
#                                 )
# item_list: list = get_data_list("SUB_LOCATIONS",
#                                 category=category,
#                                 condition='data_list'
#                                 )
# ziped_list: list = zip(menu_list, item_list)
#
# text = f'{"Выберете нарушение нажав на кнопку соответствующего нарушения."}\n \n' + \
#        ' \n'.join(str(item[0]) + " : " + str(item[1]) for item in ziped_list)
# print(text)
#
# nd_data: list = get_data_list("NORMATIVE_DOCUMENTS",
#                               category=category,
#                               condition=dict_condition
#                               )
# pprint(nd_data)
#
# if not nd_data:
#     quit()
#
# violation_data = {
#     "normative_documents": nd_data[0].get('title', None),
#     "normative_documents_normative": nd_data[0].get('normative', None),
#     "normative_documents_procedure": nd_data[0].get('procedure', None)
# }
#
# pprint(violation_data)
