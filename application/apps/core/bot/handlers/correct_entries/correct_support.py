from __future__ import annotations

from datetime import datetime
from pprint import pprint

from aiogram import types
from pandas import DataFrame

from apps.MyBot import bot_send_message
from apps.core.bot.messages.messages import Messages, LogMessage
from apps.core.database.db_utils import db_get_table_headers, db_get_data_list
from loader import logger


class Spotter(object):

    def __new__(cls, *args, **kwargs):
        # logger.info(f"Hello from {Report.__new__}")
        return super().__new__(cls)

    def __init__(self):
        self.spotter_data: dict[str, str] = {}

    def _print(self):
        pprint(self._spotter_data)

    @property
    def spotter_data(self):
        return self._spotter_data

    @spotter_data.setter
    def spotter_data(self, value):
        self._spotter_data = value
        if value == {}:
            return
        self._print()


spotter_data = Spotter().spotter_data


async def clear_spotter():
    """

    :return:
    """
    try:
        spotter_data.clear()
        return True

    except Exception as err:
        logger.error(f"Error clearing spot {repr(err)}")
        return False


async def create_user_dataframe(hse_user_id: str, violations_dataframe: DataFrame) -> DataFrame or None:
    """Получение данных пользователя"""

    logger.debug(f'{hse_user_id = }')

    # if violations_dataframe.empty:
    #     logger.error(f'{Messages.Error.dataframe_is_empty}')
    #     return None

    if not await check_dataframe(violations_dataframe, hse_user_id):
        return None

    user_violations_dataframe = violations_dataframe.copy(deep=True)
    user_violations: DataFrame = user_violations_dataframe.loc[user_violations_dataframe['user_id'] == str(hse_user_id)]

    # if user_violations.empty:
    #     logger.error(f'{Messages.Error.dataframe_is_empty}  \n{user_violations = }')
    #     return None

    if not await check_dataframe(user_violations, hse_user_id):
        return None

    return user_violations


async def create_lite_dataframe_from_query(query: str, table_name: str) -> DataFrame or None:
    """Возвращает list с нарушениями

    :return: DataFrame or None
    """
    if not query:
        logger.error(f"{LogMessage.Check.no_query} ::: {await get_now()}")
        return None

    violations_data: list = await db_get_data_list(query=query)

    if not violations_data:
        logger.debug(f"{LogMessage.Check.no_violations} ::: {await get_now()}")
        return None

    headers = await db_get_table_headers(table_name=table_name)
    clean_headers: list = [item[1] for item in headers]

    try:
        dataframe = DataFrame(violations_data, columns=clean_headers)
        return dataframe
    except Exception as err:
        logger.error(f"create_dataframe {repr(err)}")
        return None


async def check_dataframe(dataframe: DataFrame, hse_user_id: str | int) -> bool:
    """Проверка dataframe на наличие данных

    :param dataframe:
    :param hse_user_id:
    :return:
    """
    if dataframe is None:
        text_violations: str = 'Незакрытых записей вне актов не обнаружено!'
        await bot_send_message(chat_id=hse_user_id, text=text_violations)
        return False

    if dataframe.empty:
        logger.error(f'{hse_user_id = } {Messages.Error.dataframe_is_empty}')
        return False

    return True


async def get_now() -> str:
    """Возвращает текущую дату и время.
    :return: str
    """
    return datetime.now().strftime("%d.%m.%Y %H:%M:%S")


async def get_item_number_from_call(call: types.CallbackQuery, hse_user_id: str | int) -> int:
    """Получение номера из call.message

    :param hse_user_id:
    :param call:
    :return:
    """
    if not call:
        await bot_send_message(chat_id=hse_user_id, text=Messages.Error.error_call)
        return 0

    if not call.message.values['text']:
        await bot_send_message(chat_id=hse_user_id, text=Messages.Error.error_call_text)
        return 0

    item_number_text = call.message.values['text'].split('_')[-1]
    logger.debug(f'{hse_user_id = } {item_number_text = }')

    try:
        item_number_text = int(item_number_text)
        return item_number_text

    except Exception as err:
        logger.error(f'{hse_user_id = } {repr(err)} {item_number_text = }')
        await bot_send_message(chat_id=hse_user_id, text=Messages.Error.error_command)
        await bot_send_message(chat_id=hse_user_id, text=Messages.Error.error_action)
        return 0


async def check_spotter_data() -> bool:
    """

    :return:
    """

    prefix: str = spotter_data.get('calld_prefix', None)
    if prefix is None:
        logger.error(f'{prefix}')
        return False

    table_name: str = spotter_data.get('character_table_name', None)
    if table_name is None:
        logger.error(f'Item {table_name} is None. return')
        return False

    user_id: str = spotter_data.get('hse_user_id', None)
    if user_id is None:
        logger.error(f'{user_id}')
        return False

    item_number: str = spotter_data.get('item_number_text', None)
    if item_number is None:
        logger.error(f'{item_number}')
        return False

    character: str = spotter_data.get('character', None)
    if character is None:
        logger.error(f'{character}')
        return False

    return True
