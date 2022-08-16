import os
from os import makedirs

from apps.core.bot.utils.json_worker.read_json_file import read_json_file
from apps.core.bot.utils.json_worker.writer_json_file import write_json_file
from loader import logger


async def normalize_violation_data(violation: dict) -> dict:
    """Обработка данных в записях не соответствующих записям в DataBase

    :param violation: dict  с данными для нормализации
    :return: normalize_violation_dict
    """

    if violation.get("year") == '2021' and violation.get("name") == 'Коршаков Алексей Сергеевич':
        violation['location'] = 'Ст. Аминьевская'

    dict_general_contractor = {
        "МИП - Строй 1(?)": "МИП-Строй№1(?)",
        "'МИП-Строй№1(?)": "МИП-Строй№1(?)",
        "'Прочее'(?)": "Прочее",
        "'Прочее'(?)'": "Прочее",
        "Прочее(?)": "Прочее",
        "'Прочее(?)": "Прочее",
        "СиАрСиСи Рус(?)": "СиАрСиСи(?)",
        "'СиАрСиСи'(?)": "СиАрСиСи(?)",
        "'МИП-С№1('ССМ')": "МИП-С№1('ССМ')",
        "'СиАрСиСи'('РБТ')": "СиАрСиСи('РБТ')",
        "'СиАрСиСи'('РСКМ')": "СиАрСиСи(РСКМ)",
        "'СиАрСиСи'('Стройком')": "СиАрСиСи('Стройком')",
        "'МИП-С№1('Строй-монтаж2002')": "МИП-С№1('Строй-монтаж2002')",
        "'МИП-С№1('ТрансЭнергоСнаб')": "МИП-С№1('ТрансЭнергоСнаб')",
        "'ГорИнжПроект'(?)": "ГорИнжПроект(?)",
        "'ЛУЧ'(?)": "ЛУЧ(?)",
        "ОАО Ф.С.Г. ЦентрСтрой": "ФСГ ЦентрСтрой",
        "'МИП-С№1('ЕСТ')": "МИП-С№1(ЕСТ)",
    }

    general_contractor = violation.get("general_contractor", None)
    violation["general_contractor"] = dict_general_contractor.get(general_contractor, general_contractor)

    dict_main_category = {
        "Промышленная безопасность_+": "Промышленная безопасность",
        "Электробезопасность_": "Электробезопасность",
        "Экология_": "Отходы",
        "Работы на высоте_": "Работы на высоте",
    }

    main_category = violation.get("main_category", None)
    violation["main_category"] = dict_main_category.get(main_category, main_category)

    dict_category = {
        "Электробезопасность_": "Электробезопасность",
        "Экология_": "Отходы",
        "Работы на высоте_": "Работы на высоте",
        "Дежурное освещение": "Освещение",
        "Охрана труда_": "Другое",
        "Обучени, аттестация/квалификация": "Обучение аттестация/квалификация",
        "Пожарная безопасность_": "Огневые работы",
        "Обучения и инструктажи_": "Обучение аттестация/квалификация",
        "Не безопасное состояние": "Другое",
        "Не безопасное поведение_": "Другое",
        "Огневые работы_": "Огневые работы",
        "Складирование материалов ГСМ_": "Складирование",
    }
    category = violation.get("category", None)
    violation["category"] = dict_category.get(category, category)

    dict_status = {
        "Устранено": "Завершено",
        None: 'Завершено',
    }
    status = violation.get("status", "Завершено")
    violation["status"] = dict_status.get(status, status)

    dict_location = {
        "Аминьевское шоссе": "Ст. Аминьевская",
        "Кунцевская (Можайская)": "Ст. Кунцевская",
        "станция метро Аминьевская": "Ст. Аминьевская",
        "Нкц": "Национальный космический центр",
    }
    location = violation.get("location", None)
    violation["location"] = dict_location.get(location, location)

    dict_work_shift = {
        "ночная смена": "Ночная смена",
        "Дневная": "Дневная смена",
        "null": "Дневная смена",
        None: "Дневная смена",

    }

    workshift = violation.get("work_shift", None)
    violation["work_shift"] = dict_work_shift.get(workshift, workshift)

    dict_violation_category = {
        "Акт-предписание*": "Опасная ситуация*",
        "LTI*": "LTI (травма с врем. потерей труд-ти)",
    }

    violation_category = violation.get("violation_category", None)
    violation["violation_category"] = dict_violation_category.get(violation_category, violation_category)

    dict_incident_level = {
        "/cancel": "Без последствий",
        "/generate": "Без последствий",
    }
    incident_level = violation.get("incident_level", None)
    violation["incident_level"] = dict_incident_level.get(incident_level, incident_level)

    return violation


async def write_json(violation):
    """Запись в файл"""
    if not os.path.isfile(violation['json_full_name']):
        print(f"FileNotFoundError {violation['json_full_name']} ")

    date_violation = violation['file_id'].split('___')[0]

    violation['json_full_name'] = \
        f"C:\\Users\\KDeusEx\\PycharmProjects\\SWTS\\application\\media\\{violation['user_id']}\\data_file" \
        f"\\{date_violation}\\json\\report_data___{violation['file_id']}.json"

    await create_file_path(
        f"C:\\Users\\KDeusEx\\PycharmProjects\\SWTS\\application\\media\\{violation['user_id']}\\data_file"
        f"\\{date_violation}\\json\\"
    )
    violation['photo_full_name'] = \
        f"C:\\Users\\KDeusEx\\PycharmProjects\\SWTS\\application\\media\\{violation['user_id']}\\data_file" \
        f"\\{date_violation}\\photo\\report_data___{violation['file_id']}.jpg"

    await create_file_path(
        f"C:\\Users\\KDeusEx\\PycharmProjects\\SWTS\\application\\media\\{violation['user_id']}\\data_file"
        f"\\{date_violation}\\photo\\"
    )

    await write_json_file(data=violation, name=violation['json_full_name'])


async def create_file_path(path: str):
    """Проверка и создание путей папок и файлов
    :param path:
    :return:
    """
    if not os.path.isdir(path):
        # logger.info(f"user_path{path} is directory")
        try:
            makedirs(path)
        except Exception as err:
            logger.info(f"makedirs err {repr(err)}")


async def data_violation_completion(violation_file: str, params: dict) -> tuple[int, dict]:
    """
    :param

    """
    error_counter: int = 0
    # comment_counter: int = 0
    # act_required_counter: int = 0
    # elimination_time_counter: int = 0
    # general_contractor_counter: int = 0
    # incident_level_counter: int = 0

    violation = await read_json_file(file=violation_file)
    user_data_json_file = await read_json_file(file=params['user_file'])
    file_id = violation.get('file_id')

    if not violation.get("work_shift"):
        violation["work_shift"] = user_data_json_file.get("work_shift")

    if not violation.get("function"):
        violation["function"] = user_data_json_file.get("function")

    if not violation.get("name"):
        violation["name"] = user_data_json_file.get("name")

    if not violation.get("parent_id"):
        violation["parent_id"] = user_data_json_file.get("parent_id")

    if not violation.get("location"):
        violation["location"] = user_data_json_file.get("name_location")

    if not violation.get("status"):
        print(f"ERROR file: {file_id} don't get 'status' parameter")
        error_counter += 1
        violation["status"] = 'Завершено'

    if not violation.get("violation_id"):
        print(f"ERROR file: {file_id} don't get 'violation_id' parameter")
        error_counter += 1
        violation["violation_id"] = violation['file_id'].split('___')[-1]

    if not violation.get("json_folder_id"):
        print(f"ERROR file: {file_id} don't get 'json_folder_id' parameter")
        error_counter += 1
        violation["json_folder_id"] = '0'

    if not violation.get('general_contractor'):
        print(f"ERROR file: {file_id} don't get 'general_contractor' parameter")
        error_counter += 1

        # general_contractor_counter += 1
        # os.remove(violation_file)
        # print(f"file: {violation_file} is remove")

    if not violation.get('elimination_time'):
        print(f"ERROR file: {file_id} don't get 'elimination_time' parameter")
        error_counter += 1
        # elimination_time_counter += 1
        violation['elimination_time'] = '1 день'

    if not violation.get('incident_level'):
        print(f"ERROR file: {file_id} don't get 'incident_level' parameter")
        error_counter += 1
        # incident_level_counter += 1
        violation['incident_level'] = 'Без последствий'
        await write_json(violation=violation)

    if not violation.get('act_required'):
        print(f"ERROR file: {file_id} don't get 'act_required' parameter")
        error_counter += 1
        # act_required_counter += 1
        violation['act_required'] = 'Не требуется*'

    if not violation.get('comment'):
        print(f"ERROR file: {file_id} don't get 'comment' parameter")
        error_counter += 1
        # comment_counter += 1

    # print(f"general_contractor_counter {general_contractor_counter} in {error_counter} items")
    # print(f"elimination_time_counter {elimination_time_counter} in {error_counter} items")
    # print(f"act_required_counter {act_required_counter} in {error_counter} items")
    # print(f"incident_level_counter {incident_level_counter} in {error_counter} items")
    # print(f"comment_counter {comment_counter} in {error_counter} items")

    await write_json(violation=violation)

    return error_counter, violation
