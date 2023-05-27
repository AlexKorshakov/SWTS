from __future__ import annotations

import os

from pandas import DataFrame

from apps.core.bot.handlers.correct_entries.correct_support import create_lite_dataframe_from_query, check_dataframe
from apps.core.database.db_utils import db_update_column_value, db_get_dict_userdata, \
    db_get_data_dict_from_table_with_id
from apps.core.database.query_constructor import QueryConstructor
from apps.core.utils.json_worker.read_json_file import read_json_file
from apps.core.utils.json_worker.writer_json_file import write_json_file
from apps.core.utils.secondary_functions.get_filepath import BOT_MEDIA_PATH, REGISTRY_NAME
from config.config import WRITE_DATA_ON_GOOGLE_DRIVE
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
                                       hse_user_id: str | int, v_df: DataFrame = None) -> bool:
    """Внесение изменений в файл json на сервере

    :param v_df:
    :param item_number: str | int
    :param column_name: str
    :param item_value: str | int
    :param hse_user_id: str | int
    :return: bool
    """

    if not await check_dataframe(v_df, hse_user_id):
        query_kwargs: dict = {
            "action": 'SELECT', "subject": '*',
            "conditions": {
                "id": item_number,
            },
        }
        query: str = await QueryConstructor(None, 'core_violations', **query_kwargs).prepare_data()

        v_df: DataFrame = await create_lite_dataframe_from_query(query=query, table_name='core_violations')

        if not await check_dataframe(v_df, hse_user_id):
            return False

    v_df[column_name] = item_value

    violation_data: dict = v_df.to_dict()
    violation_data = {key: value.get(0, None) for (key, value) in violation_data.items() if value is not None}

    if not violation_data.get('json', None):
        return False

    violation_read_json = await read_json_file(file=f"{BOT_MEDIA_PATH}{violation_data.get('json', None)}")
    violation_data.update(violation_read_json)

    if not await write_json_file(data=violation_data, name=f"{BOT_MEDIA_PATH}{violation_data.get('json', None)}"):
        return False

    return True


async def update_column_value_in_google_disk(*, item_number: str | int, column_name: str, item_value: str | int,
                                             hse_user_id: str | int) -> bool:
    if not WRITE_DATA_ON_GOOGLE_DRIVE:
        logger.info(f'{WRITE_DATA_ON_GOOGLE_DRIVE = } abort upload / download from Google Drive')

    return True
