import io
import json

from loader import logger

SUFFIX: str = ".json"


async def write_json_file(*, data: dict = None, name: str = "") -> None:
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


async def write_json_violation_user_file(*, data: dict = None) -> bool:
    """Запись данных о нарушениях в json
    """
    name = str(data["json_full_name"])

    await write_json(name=name, data=data)
    return True


async def write_json(name: str, data):
    """Запись данных в json

    :param name:
    :param data:
    :return:
    """
    try:
        with io.open(name, 'w', encoding='utf8') as outfile:
            str_ = json.dumps(data,
                              indent=4,
                              sort_keys=True,
                              separators=(',', ': '),
                              ensure_ascii=False)
            outfile.write(str_)
    except TypeError as err:
        logger.error(f" TypeError: {repr(err)}")
