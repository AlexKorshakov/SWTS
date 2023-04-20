from __future__ import annotations

from apps.core.database.db_utils import db_update_column_value
from loader import logger


async def update_column_value_in_db(*, item_number: str | int, column_name: str, item_value: str | int,
                                    hse_user_id: str | int) -> bool:
    """

    :return:
    """

    status_result_execute: bool = await db_update_column_value(
        column_name=column_name,
        value=item_value,
        violation_id=str(item_number)
    )
    if not status_result_execute:
        logger.error(f'{hse_user_id = } Ошибка обновления данных {item_number}  в database!')
        return False

    logger.info(f'{hse_user_id = } Данные записи {item_number} успешно обновлены в database!')
    return True


async def update_column_value_in_local(*, item_number: str | int, column_name: str, item_value: str | int,
                                       hse_user_id: str | int) -> bool:
    return False


async def update_column_value_in_google_disk(*, item_number: str | int, column_name: str, item_value: str | int,
                                             hse_user_id: str | int) -> bool:
    return False


