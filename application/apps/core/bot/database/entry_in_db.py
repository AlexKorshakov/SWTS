import asyncio
from loader import logger

from apps.core.bot.database.DataBase import DataBase


async def write_data_in_database(*, violation_data: dict) -> bool:
    """Поиск записи по file_id в database

    :param violation_data:
    :return: True or False
    """

    if not violation_data.get('file_id'):
        logger.error(f"Error get file_id for violation_data: {violation_data}")
        return False

    try:
        if not DataBase().violation_exists(violation_data.get('file_id')):
            DataBase().add_violation(violation=violation_data)
            return True
    except Exception as err:
        logger.error(f"Error add_violation in DataBase() : {repr(err)}")
        return False

    return False


async def test():
    # google_drive_service = await drive_account_credentials()
    logger.info(f'{DataBase().db_file}')


if __name__ == "__main__":
    asyncio.run(test())
