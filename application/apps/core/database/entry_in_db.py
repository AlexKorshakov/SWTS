from sqlite3 import OperationalError

from loader import logger

logger.debug(f"{__name__} start import")
from apps.core.database.db_utils import (db_add_violation,
                                         db_check_record_existence)

logger.debug(f"{__name__} finish import")


async def write_data_in_database(*, violation_data: dict) -> bool:
    """Поиск записи по file_id в database

    :param violation_data:
    :return: True or False
    """

    if not violation_data.get('file_id'):
        logger.error(f"Error get file_id for violation_data: {violation_data}")
        return False

    try:
        if not await db_check_record_existence(file_id=violation_data.get('file_id')):
            if await db_add_violation(violation_data=violation_data):
                return True

    except OperationalError as err:
        logger.error(f"Error add_violation in DataBase() : {repr(err)}")
        return False

    except Exception as err:
        logger.error(f"Error add_violation in DataBase() : {repr(err)}")
        return False

    return False

# async def test():
#     # google_drive_service = await drive_account_credentials()
#     logger.info(f'{DataBase().db_file}')
#
#
# if __name__ == "__main__":
#     asyncio.create_qr_code(test())
