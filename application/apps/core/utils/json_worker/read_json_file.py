import json


async def read_json_file(file: str):
    """Получение данных из json.

    :param file: полный путь к файлу
    """
    try:
        with open(file, 'r', encoding='utf8') as data_file:
            data_loaded = json.load(data_file)
        return data_loaded
    except FileNotFoundError:
        return None


async def read_json_files(files: list, data: list) -> list:
    """Получение данных множества jsons и запись данных в data

    :param files: список полных имён / путей к файлам
    :param data: входящий list
    :return: data
    """

    for item in files:
        data.append(await read_json_file(item))

    return data
