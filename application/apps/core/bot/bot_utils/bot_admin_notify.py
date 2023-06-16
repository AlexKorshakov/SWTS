from loader import logger

logger.debug(f"{__name__} start import")
from pandas import DataFrame
import asyncio
from aiogram.utils.exceptions import NetworkError
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiohttp import ClientConnectorError

from apps.core.database.db_utils import db_get_table_headers, db_get_data_list
from apps.core.database.query_constructor import QueryConstructor
from apps.xxx import assistant

logger.debug(f"{__name__} finish import")


async def admin_notify(user_id, notify_text: str, button: InlineKeyboardButton = None) -> bool:
    """Уведомление админов
    """

    logger.info(f"{notify_text = }")
    try:
        reply_markup = InlineKeyboardMarkup()
        reply_markup.add(InlineKeyboardButton(text=f'{user_id}', url=f"tg://user?id={user_id}"))
        if button:
            reply_markup.add(button)

        for bot_admin in await get_admin_id_list():
            await assistant.send_message(chat_id=bot_admin, text=notify_text, reply_markup=reply_markup)
        return True

    except (NetworkError, ClientConnectorError) as err:
        logger.error(f'{user_id = } connect err {repr(err)}')
        logger.error(f'User {user_id} ошибка уведомления ADMIN_ID {repr(err)}')
        return False

    except Exception as err:
        logger.error(f'User {user_id} ошибка уведомления ADMIN_ID {repr(err)}')
        return False


async def test2():
    user_id: str = '373084462'
    notify_text: str = f'User {user_id} попытка доступа к функциям без регистрации'
    button = InlineKeyboardButton(text=f'{user_id}', url=f"tg://user?id={user_id}")
    answer: bool = await admin_notify(user_id, notify_text, button)
    print(answer)


if __name__ == "__main__":
    asyncio.run(test2())
