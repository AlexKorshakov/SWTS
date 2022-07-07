from loader import logger

from config.config import BD_FILE
from apps.core.bot.database.DataBase import DataBase


async def entry_in_db(*, violation_data) -> bool:
    """Поиск в database
    :param violation_data:
    :return:
    """

    if not violation_data.get('file_id'):
        logger.error(f"Error get file_id for violation_data: {violation_data}")
        return False

    try:
        if not DataBase(db_file=BD_FILE).violation_exists(violation_data.get('file_id')):
            DataBase(db_file=BD_FILE).add_violation(violation=violation_data)
            return True
    except Exception as err:
        logger.error(f"Error add_violation in DataBase() : {repr(err)}")
        return False

    return False
