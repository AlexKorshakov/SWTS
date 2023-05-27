import asyncio

from aiogram import Dispatcher
from pandas import DataFrame

from apps.core.database.db_utils import db_get_data_list, db_get_table_headers
from loader import logger


async def on_startup_notify(dp: Dispatcher) -> bool:
    logger.info("Оповещение администрации...")

    kwargs: dict = {
        "action": 'SELECT',
        "subject": 'hse_telegram_id',
        "conditions": {
            "lazy_query": "`hse_role_is_admin` = 1",
        },
    }
    query: str = await QueryConstructor(table_name='core_hseuser', **kwargs).prepare_data()
    admins_datas: list = DataBase().get_data_list(query=query)

    if not admins_datas:
        try:
            await dp.bot.send_message(ADMIN_ID, "Бот был успешно запущен", disable_notification=True)
            logger.info(f"Сообщение отправлено {ADMIN_ID}")
            return True
        except Exception as err:
            logger.error(f"Чат с админом не найден {err} ")
            return False

    admins_datas = [item[0] for item in admins_datas if item]

    for num, hse_telegram_id in enumerate(admins_datas, start=1):

        if not hse_telegram_id:
            logger.debug(f"Значение не найдено {num = } for {len(hse_role_is_admins_list)} {hse_telegram_id = }")
            continue
        if hse_telegram_id not in hse_role_receive_notifications_list:
            logger.debug(f"Значение не найдено {num = } for {len(hse_role_is_admins_list)} {hse_telegram_id = }")
            continue

        try:
            await dp.bot.send_message(hse_telegram_id, "Бот был успешно запущен", disable_notification=True)
            logger.info(f"Сообщение отправлено {hse_telegram_id}")
            await asyncio.sleep(0.5)
        except Exception as err:
            logger.error(f"Чат {num = } с админом {hse_telegram_id} не найден {err = } ")

    return True


async def test():
    dp: Dispatcher = None
    await on_startup_notify(dp)


if __name__ == '__main__':
    asyncio.run(test())
