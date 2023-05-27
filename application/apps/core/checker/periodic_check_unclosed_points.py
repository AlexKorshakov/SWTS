import asyncio
from datetime import datetime

from pandas import DataFrame

from loader import logger
from apps.MyBot import MyBot
from apps.core.bot.messages.messages import LogMessage, Messages
from apps.core.database.db_utils import db_get_table_headers, db_get_data_list, db_get_data_dict_from_table_with_id
from apps.core.database.query_constructor import QueryConstructor


async def periodic_check_unclosed_points():
    """Периодическая проверка незакрытых пунктов и актов"""

    offset: int = -7

    while True:
        await asyncio.sleep(1)

        now = datetime.now()
        if 18 + offset > now.hour + 1 > 9 + offset:

            result_check_list: bool = await check_acts_prescriptions_status()

            if result_check_list:
                logger.info(f"{LogMessage.Check.periodic_check_unclosed_points} ::: {await get_now()}")
            else:
                logger.error(
                    f'{__name__} error check_acts_prescriptions_status {result_check_list = } '
                    f'::: {await get_now()}'
                )

        else:
            logger.info(f"{LogMessage.Check.time_period_error} ::: {await get_now()}")

        await asyncio.sleep(60 * 60 * 12)


async def check_acts_prescriptions_status() -> bool:
    """Проверка поля status acts

    :return:
    """
    query_kwargs: dict = {
        "action": 'SELECT',
        "subject": '*',
        "conditions": {
            "finished_id": "!= 1",
            "status_id": "!= 1",
        },
    }
    query: str = await QueryConstructor(None, 'core_violations', **query_kwargs).prepare_data()

    violations_dataframe: DataFrame = await create_lite_dataframe_from_query(query=query, table_name='core_violations')
    if violations_dataframe.empty:
        logger.error(f'{Messages.Error.dataframe_is_empty}  \n{query = }')
        return False

    unique_hse_user_ids: list = violations_dataframe.user_id.unique().tolist()
    logger.debug(
        # f'{__name__} {await say_fanc_name()} {unique_hse_user_ids = }'
        f'{unique_hse_user_ids = }'
    )

    if not unique_hse_user_ids:
        return False

    hse_role_receive_notifications_list: list = await get_hse_role_receive_notifications_list()

    for hse_user_id in unique_hse_user_ids:
        # if hse_user_id != '373084462': continue

        if int(hse_user_id) not in hse_role_receive_notifications_list:
            continue

        user_violations: DataFrame = await create_user_dataframe(hse_user_id, violations_dataframe)
        if user_violations.empty:
            return False

        unique_acts_numbers: list = user_violations.act_number.unique().tolist()
        len_unique_acts_numbers: int = len(unique_acts_numbers)
        logger.debug(
            f'{hse_user_id = } len {len_unique_acts_numbers} {unique_acts_numbers = }'
        )

        text_violations = await text_processor_user_violations(user_violations)

        await MyBot.bot.send_message(chat_id=hse_user_id, text=text_violations)

    return True


async def get_hse_role_receive_notifications_list() -> list:
    """Получение списка пользователей кому отправляются уведомления
    """

    db_table_name: str = 'core_hseuser'
    query: str = f'SELECT * FROM {db_table_name}'
    datas_query: list = await db_get_data_list(query=query)

    if not datas_query:
        return []

    if not isinstance(datas_query, list):
        return []

    clean_headers: list = [item[1] for item in await db_get_table_headers(table_name=db_table_name)]
    if not clean_headers:
        return []

    try:
        hse_role_receive_df: DataFrame = DataFrame(datas_query, columns=clean_headers)
    except Exception as err:
        logger.error(F"create_dataframe {repr(err)}")
        return []

    current_act_violations_df: DataFrame = hse_role_receive_df.loc[
        hse_role_receive_df['hse_role_receive_notifications'] == 1
        ]

    unique_hse_telegram_id: list = current_act_violations_df.hse_telegram_id.unique().tolist()

    return unique_hse_telegram_id


async def text_processor_user_violations(user_violations: DataFrame) -> str:
    """Формирование текста для отправки пользователю"""

    unique_acts_numbers: list = user_violations.act_number.unique().tolist()

    act_description: list = []
    len_unique_acts: int = 0
    for act_number in unique_acts_numbers:

        if not act_number:
            continue

        act_violations_df = user_violations.copy(deep=True)
        current_act_violations: DataFrame = act_violations_df.loc[act_violations_df['act_number'] == act_number]

        unclosed_points_df = current_act_violations.loc[current_act_violations['status_id'] != 1]
        unclosed_points: int = len(unclosed_points_df)

        item_info = f'Ном: {act_number} всего пунктов: {len_act_violations} Незакрыто: {unclosed_points}'
        act_description.append(item_info)
        len_unique_acts += 1

    non_acts_items_df: DataFrame = user_violations.loc[user_violations['act_number'] == '']
    non_acts_items: int = len(non_acts_items_df)
    non_acts_text: str = f'Записей вне актов всего: {non_acts_items}'

    header_text: str = f'У вас есть незакрытые акты: Всего актов {len_unique_acts}'
    footer_text: str = 'Для действий выберите в меню соответствующую команду(/correct_entries)'

    acts_text: str = '\n'.join(act_description)

    final_text: str = f'{header_text} \n\n{acts_text} \n\n{non_acts_text} \n\n{footer_text}'
    return final_text


async def create_user_dataframe(hse_user_id: int, violations_dataframe: DataFrame) -> DataFrame or None:
    """Получение данных пользователя"""

    if violations_dataframe.empty:
        logger.error(f'{Messages.Error.dataframe_is_empty}')
        return None

    user_violations_dataframe = violations_dataframe.copy(deep=True)
    user_violations: DataFrame = user_violations_dataframe.loc[user_violations_dataframe['user_id'] == hse_user_id]

    if user_violations.empty:
        logger.error(f'{Messages.Error.dataframe_is_empty}  \n{user_violations = }')
        return None

    return user_violations


async def get_item_title_for_id(table_name: str, item_id: int, item_name: str = None) -> str:
    """

    :param item_name:
    :param table_name:
    :param item_id:
    :return:
    """
    item_dict: dict = await db_get_data_dict_from_table_with_id(
        table_name=table_name,
        post_id=item_id
    )

    item_name = item_name if item_name else 'title'
    item_text: str = item_dict.get(item_name, '')
    return item_text


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


async def get_now() -> str:
    """Возвращает текущую дату и время.
    :return: str
    """
    return datetime.now().strftime("%d.%m.%Y %H:%M:%S")


# async def say_fanc_name():
#     stack = traceback.extract_stack()
#     return str(stack[-2][2])


async def test():
    await periodic_check_unclosed_points()


if __name__ == '__main__':
    asyncio.run(test())
