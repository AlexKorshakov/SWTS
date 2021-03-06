import inspect
import json
import os.path
from json import JSONDecodeError

from loader import logger

filename = inspect.getframeinfo(inspect.currentframe()).filename
path = os.path.dirname(os.path.abspath(filename))

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


def get_names_from_json(name: str = None) -> list:
    """ Функция получения настроек из файла json.
    :return: list
    """
    if not name:
        return []

    try:
        with open(path + "\\" + name + ".json", "r", encoding="UTF-8") as read_file:
            list_value = json.loads(read_file.read())
            if not list_value:

                if name not in [key for key, value in ALL_CATEGORY.items()]:
                    return []

                return ALL_CATEGORY[name]

            return list_value

    except (FileNotFoundError, JSONDecodeError) as err:
        logger.error(f" {name} {repr(err)}")
        return []
