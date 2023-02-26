import asyncio

from aiogram import Dispatcher

from apps.core.database.DataBase import DataBase
from apps.core.database.query_constructor import QueryConstructor
from config.config import ADMIN_ID
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
    if admins_datas:
        admins_datas = [item[0] for item in admins_datas if item]

    # table_name = 'core_hseuser'
    # headers = DataBase().get_table_headers(table_name=table_name)
    # clean_headers: list = [item[1] for item in headers]

    if not admins_datas:
        try:
            await dp.bot.send_message(ADMIN_ID, "Бот был успешно запущен", disable_notification=True)
            logger.info(f"Сообщение отправлено {ADMIN_ID}")
            return True
        except Exception as err:
            logger.error(f"Чат с админом не найден {err} ")
            return False

    for num, hse_telegram_id in enumerate(admins_datas, start=1):
        # adm_data: dict = dict(zip(clean_headers, adm_data))
        # hse_telegram_id = adm_data.get('id', None)
        # hse_telegram_id =adm_data[0]

        if not hse_telegram_id:
            logger.debug(f"Значение не найдено {num = } for {len(admins_datas)} {hse_telegram_id = }")
            continue

        try:
            await dp.bot.send_message(hse_telegram_id, "Бот был успешно запущен", disable_notification=True)
            logger.info(f"Сообщение отправлено {hse_telegram_id}")
            await asyncio.sleep(0.3)
        except Exception as err:
            logger.error(f"Чат с админом {hse_telegram_id} не найден {err = } ")
    return True


async def test():
    dp: Dispatcher = None
    await on_startup_notify(dp)


if __name__ == '__main__':
    asyncio.run(test())
