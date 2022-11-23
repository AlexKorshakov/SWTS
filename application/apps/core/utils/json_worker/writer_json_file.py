import io
import json

from loader import logger

SUFFIX: str = ".json"


async def write_json_file(*, data: dict = None, name: str = None) -> None:
    """Запись данных в json

    :param name: полный путь к файлу
    :param data: dict  с данными для записи
    """
    await write_json(name=name, data=data)


async def write_user_registration_data_on_json_on_local_storage(*, user_data: dict = None) -> bool:
    """Запись данных в json
    """
    name = user_data['reg_json_full_name']

    await write_json(name=name, data=user_data)
    return True


async def write_json_violation_user_file(*, data: dict = None, json_full_name: str = None) -> bool:
    """Запись данных о нарушениях в json

    :param json_full_name: полный путь для записи / сохранения файла включая расширение,
    :param data: данные для записи / сохранения
    :return: True or False
    """
    if not json_full_name:
        json_full_name = str(data["json_full_name"])

    if await write_json(name=json_full_name, data=data):
        logger.debug(f'Data write on {json_full_name}')
        return True
    return False


async def write_json(name: str, data) -> bool:
    """Запись данных в json

    :param name: полный путь для записи / сохранения файла включая расширение,
    :param data: данные для записи / сохранения
    :return: True or False
    """
    try:
        with io.open(name, 'w', encoding='utf8') as outfile:
            str_ = json.dumps(data,
                              indent=4,
                              sort_keys=True,
                              separators=(',', ': '),
                              ensure_ascii=False)
            outfile.write(str_)
            return True
    except TypeError as err:
        logger.error(f"TypeError: {repr(err)}")
        return False
