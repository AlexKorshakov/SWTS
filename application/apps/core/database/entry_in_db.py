import os
from pathlib import Path

from apps.core.utils.json_worker.read_json_file import read_json_file
from loader import logger

logger.debug(f"{__name__} start import")
import asyncio
from sqlite3 import OperationalError
from apps.core.database.db_utils import (db_add_violation,
                                         db_check_record_existence)

logger.debug(f"{__name__} finish import")


async def write_data_in_database(*, violation_data_to_db: dict) -> bool:
    """Поиск записи по file_id в database

    :param violation_data_to_db:
    :return: True or False
    """

    if not violation_data_to_db.get('file_id'):
        logger.error(f"Error get file_id for violation_data: {violation_data_to_db}")
        return False

    try:
        if not await db_check_record_existence(file_id=violation_data_to_db.get('file_id')):
            if await db_add_violation(violation_data=violation_data_to_db):
                return True

    except OperationalError as err:
        logger.error(f"Error add_violation in DataBase() : {repr(err)}")
        return False

    except Exception as err:
        logger.error(f"Error add_violation in DataBase() : {repr(err)}")
        return False

    return False


async def qr_get_file_path(*args) -> str:
    """

    :param args:
    :return:
    """
    return str(Path(*args))


async def get_files(folder_path: str) -> list:
    """

    :param folder_path:
    :return:
    """
    if not folder_path:
        return []

    for _, _, files in os.walk(folder_path):
        return files


async def test():
    """

    :return:
    """
    media_path: str = 'C:\\Users\\KDeusEx\\PycharmProjects\\!media\\373084462\\data_file\\07.10.2023\\json'
    matrix_folder_path: str = await qr_get_file_path(media_path)
    files: list = await get_files(str(matrix_folder_path))

    violations_data = []
    for file in files:
        data_dict = await read_json_file(f'{media_path}\\{file}')
        data_dict['general_contractor'] = 'ООО Ренейссанс Хэви Индастрис'

        violations_data.append(data_dict)

    for data_dict in violations_data:
        await write_data_in_database(violation_data_to_db=data_dict)


if __name__ == "__main__":
    asyncio.run(test())
