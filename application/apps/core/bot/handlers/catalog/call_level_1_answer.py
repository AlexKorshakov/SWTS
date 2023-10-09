from __future__ import annotations

from aiogram import types
from pandas import DataFrame

from apps.MyBot import MyBot, bot_send_message
from apps.core.bot.bot_utils.check_user_registration import check_user_access
# from apps.core.bot.data.board_config import board_config
from apps.core.bot.handlers.catalog.catalog_func_handler import catalog_spot_data
from apps.core.bot.handlers.catalog.catalog_support import get_dataframe, get_level_1_list_dict, get_nan_value_text, \
    text_processor_level, text_processor, list_number, level_1_column, level_2_column
from apps.core.bot.keyboards.inline.build_castom_inlinekeyboard import build_inlinekeyboard
from apps.core.bot.messages.messages import Messages
from loader import logger


@MyBot.dp.callback_query_handler(lambda call: 'level_1__' in call.data)
async def call_level_1_answer(call: types.CallbackQuery, user_id: int | str = None) -> None:
    """Обработка ответов
    """
    hse_user_id = call.message.chat.id if call else user_id
    logger.debug(f'{hse_user_id = } {call.data = }')

    # msg_id = call.message.message_id
    # await bot_delete_message(chat_id=hse_user_id, message_id=msg_id, sleep_sec=15)

    if not await check_user_access(chat_id=hse_user_id):
        logger.error(f'access fail {hse_user_id = }')
        return

    dataframe = await get_dataframe(hse_user_id, column_number=list_number)
    if not await check_dataframe(dataframe, hse_user_id=hse_user_id):
        await bot_send_message(chat_id=hse_user_id, text='Данные не найдены dataframe')
        return

    level_1_num: str = call.data
    level_1_list_dicts: list = await get_level_1_list_dict(hse_user_id, dataframe)
    level_1_name: str = [item[level_1_num] for item in level_1_list_dicts if level_1_num in item][0]

    catalog_spot_data['level_1_name'] = level_1_name

    df_level_2: DataFrame = dataframe.loc[dataframe[dataframe.columns[level_1_column]] == level_1_name]
    if not await check_dataframe(df_level_2, hse_user_id=hse_user_id):
        await bot_send_message(chat_id=hse_user_id, text='Данные не найдены dataframe')
        return

    level_2: list = df_level_2[df_level_2.columns[level_2_column]].unique().tolist()
    if not level_2:
        await bot_send_message(chat_id=hse_user_id, text='Данные не найдены level_2')
        return

    title_list: list = [f"level_2__{num}" for num, item in enumerate(level_2, start=1) if item is not None]

    menu_level = board_config.menu_level = 1
    menu_list = board_config.menu_list = title_list
    count_col = board_config.count_col = 2

    nan_value_text = await get_nan_value_text(hse_user_id, df_level_2, column_nom=level_2_column, level=2 - 1)
    text = await text_processor_level(
        df_level_2,
        # nan_value=nan_value_text,
        level=level_2_column, level_name=level_1_name
    )

    for item_txt in await text_processor(text=text):
        await bot_send_message(chat_id=hse_user_id, text=item_txt)

    reply_markup = await build_inlinekeyboard(some_list=menu_list, num_col=count_col, level=menu_level, )
    await bot_send_message(chat_id=hse_user_id, text=Messages.Choose.choose_value, reply_markup=reply_markup )


async def check_dataframe(dataframe: DataFrame, hse_user_id: str | int) -> bool:
    """Проверка dataframe на наличие данных

    :param dataframe:
    :param hse_user_id: id пользователя
    :return:
    """
    if dataframe is None:
        text_violations: str = 'не удалось получить данные!'
        logger.error(f'{hse_user_id = } {text_violations}')
        return False

    if dataframe.empty:
        logger.error(f'{hse_user_id = } {Messages.Error.dataframe_is_empty}')
        return False

    return True
