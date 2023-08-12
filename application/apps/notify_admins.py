import asyncio

from aiogram import Dispatcher
from pandas import DataFrame

# from apps.MyBot import MyBot
from apps.core.database.db_utils import db_get_data_list, db_get_table_headers
from apps.core.database.query_constructor import QueryConstructor
from loader import logger


async def on_startup_notify(dp: Dispatcher) -> bool:
    logger.info(f"{dp.bot._me.first_name}  Оповещение администрации...")

    hse_dataframe = await get_hse_dataframe()

    hse_role_is_admins_list: list = await get_hse_role_is_admins_list(
        hse_dataframe=hse_dataframe
    )

    hse_role_receive_notifications_list: list = await get_hse_role_receive_notifications_list(
        hse_dataframe=hse_dataframe
    )

    for num, hse_telegram_id in enumerate(hse_role_is_admins_list, start=1):

        if not hse_telegram_id:
            logger.debug(
                f"{dp.bot._me.first_name} Значение не найдено {num = } for {len(hse_role_is_admins_list)} {hse_telegram_id = }")
            continue
        if hse_telegram_id not in hse_role_receive_notifications_list:
            logger.debug(
                f"{dp.bot._me.first_name} Значение не найдено {num = } for {len(hse_role_is_admins_list)} {hse_telegram_id = }")
            continue

        try:
            await dp.bot.send_message(hse_telegram_id, f"{dp.bot._me.first_name} Бот был успешно запущен", disable_notification=True)
            logger.info(f"{dp.bot._me.first_name} Сообщение отправлено {hse_telegram_id}")
            await asyncio.sleep(0.5)
        except Exception as err:
            logger.error(f"{dp.bot._me.first_name} Чат {num = } с админом {hse_telegram_id} не найден {err = } ")

    return True


async def get_hse_role_is_admins_list(hse_dataframe: DataFrame) -> list:
    """Получение списка админов
    """

    current_hse_role_is_admin_df: DataFrame = hse_dataframe.loc[
        hse_dataframe['hse_role_is_admin'] == 1
        ]
    unique_hse_telegram_id: list = current_hse_role_is_admin_df.hse_telegram_id.unique().tolist()
    return unique_hse_telegram_id


async def get_hse_role_receive_notifications_list(hse_dataframe: DataFrame) -> list:
    """Получение списка пользователей кому отправляются уведомления
    """

    current_hse_role_receive_df: DataFrame = hse_dataframe.loc[
        hse_dataframe['hse_role_receive_notifications'] == 1
        ]
    unique_hse_telegram_id: list = current_hse_role_receive_df.hse_telegram_id.unique().tolist()
    return unique_hse_telegram_id


async def get_hse_dataframe() -> DataFrame or None:
    """Получение данных пользователей
    """

    table_name: str = 'core_hseuser'
    kwargs: dict = {
        "action": 'SELECT',
        "subject": '*',
    }
    query: str = await QueryConstructor(table_name=table_name, **kwargs).prepare_data()
    datas_query: list = await db_get_data_list(query=query)

    if not datas_query:
        return None

    if not isinstance(datas_query, list):
        return None

    clean_headers: list = [item[1] for item in await db_get_table_headers(table_name=table_name)]
    if not clean_headers:
        return None

    try:
        hse_role_receive_df: DataFrame = DataFrame(datas_query, columns=clean_headers)
        return hse_role_receive_df

    except Exception as err:
        logger.error(f"create_dataframe {repr(err)}")
        return None


async def test():
    dp: Dispatcher = None
    await on_startup_notify(dp)


if __name__ == '__main__':
    asyncio.run(test())
