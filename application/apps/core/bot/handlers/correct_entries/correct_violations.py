from __future__ import annotations

from aiogram import types
from pandas import DataFrame

from apps.MyBot import MyBot, bot_send_message, bot_delete_message
from apps.core.bot.bot_utils.check_user_registration import check_user_access
from apps.core.bot.data import board_config
from apps.core.bot.handlers.correct_entries.correct_non_act_item_item_correct import \
    add_act_inline_keyboard_with_action, RESULT_DICT, create_lite_dataframe_from_query
from apps.core.bot.handlers.correct_entries.correct_support_updater import update_column_value_in_db, \
    update_column_value_in_local, update_column_value_in_google_disk
from apps.core.bot.handlers.correct_entries.correct_support import spotter_data, get_item_number_from_call, \
    check_dataframe, check_spotter_data, clear_spotter
from apps.core.bot.keyboards.inline.build_castom_inlinekeyboard import build_inlinekeyboard, posts_cb
from apps.core.bot.messages.messages import Messages
from apps.core.database.query_constructor import QueryConstructor
from loader import logger


@MyBot.dp.callback_query_handler(posts_cb.filter(action=['correct_characteristic_not']))
async def call_correct_characteristic_not(call: types.CallbackQuery, callback_data: dict[str, str],
                                          user_id: int | str = None):
    """Обработка ответов содержащихся в ADMIN_MENU_LIST
    """
    hse_user_id = call.message.chat.id if call else user_id
    logger.debug(f'{hse_user_id = }')
    logger.debug(f'{callback_data = }')

    if not await check_user_access(chat_id=hse_user_id):
        logger.error(f'access fail {hse_user_id = }')
        return

    msg_id = call.message.message_id
    await bot_delete_message(chat_id=hse_user_id, message_id=msg_id, sleep_sec=15)


@MyBot.dp.callback_query_handler(lambda call: 'correct_character' in call.data)
async def call_correct_character_answer(call: types.CallbackQuery, user_id: str = None) -> None:
    """Обработка ответов
    """
    hse_user_id = call.message.chat.id if call else user_id
    logger.debug(f'{hse_user_id = }')
    logger.debug(f'{call.data = }')

    if not await check_user_access(chat_id=hse_user_id):
        logger.error(f'access fail {hse_user_id = }')
        return

    item_number_text = await get_item_number_from_call(call, hse_user_id)
    if not item_number_text: return

    character_part: list = call.message.values['text'].split('_')[1:-1]
    character: str = '_'.join(character_part)
    logger.debug(f'{hse_user_id = } {item_number_text = } {character = }')

    character_table_name = RESULT_DICT.get(character, None)

    if not character_table_name:
        logger.info(f'{hse_user_id = } {item_number_text = } {character = }')

    if character_table_name:
        query_kwargs: dict = {
            "action": 'SELECT', "subject": '*',
        }
        query: str = await QueryConstructor(None, character_table_name, **query_kwargs).prepare_data()
        table_dataframe: DataFrame = await create_lite_dataframe_from_query(
            query=query, table_name=character_table_name
        )
        if not await check_dataframe(table_dataframe, hse_user_id):
            return

        # if table_dataframe is None:
        #     text_violations: str = 'Незакрытых записей вне актов не обнаружено!'
        #     await bot_send_message(chat_id=hse_user_id, text=text_violations)
        #     return
        #
        # if table_dataframe.empty:
        #     logger.error(f'{hse_user_id = } {Messages.Error.dataframe_is_empty}  \n{query = }')
        #     return

        if 'title' not in table_dataframe.columns.values.tolist():
            return

        title_list: list = table_dataframe['title'].tolist()

        menu_level = board_config.menu_level = 1
        count_col = board_config.count_col = 1

        reply_markup = await build_inlinekeyboard(
            some_list=title_list, num_col=count_col, level=menu_level, calld_prefix=f"corr_{character_table_name}_"
        )
        await bot_send_message(
            chat_id=hse_user_id,
            text=f'Выберите значение для показателя {character} для записи item_number_{item_number_text}',
            reply_markup=reply_markup
        )
        spotter_data['calld_prefix'] = f"corr_{character_table_name}_"
        spotter_data['character_table_name'] = f"{character_table_name}"
        spotter_data['hse_user_id'] = f"{hse_user_id}"
        spotter_data['item_number_text'] = f"{item_number_text}"
        spotter_data['character'] = f"{character}"

    await bot_send_message(chat_id=hse_user_id, text=Messages.Error.error_action)

    msg_id = call.message.message_id
    await bot_delete_message(chat_id=hse_user_id, message_id=msg_id, sleep_sec=15)


@MyBot.dp.callback_query_handler(lambda call: 'characteristic_' in call.data)
async def call_characteristic_answer(call: types.CallbackQuery, user_id: str = None) -> None:
    """Обработка ответов
    """
    act_number = call.data

    hse_user_id = call.message.chat.id if call else user_id
    logger.info(f'{hse_user_id = } {call.data = }')

    text_violations = f'Выбрано {act_number}'
    reply_markup = await add_act_inline_keyboard_with_action()

    await bot_send_message(chat_id=hse_user_id, text=text_violations, reply_markup=reply_markup)

    msg_id = call.message.message_id
    await bot_delete_message(chat_id=hse_user_id, message_id=msg_id, sleep_sec=15)


@MyBot.dp.callback_query_handler(lambda call: 'corr_' in call.data)
async def call_correct_item_answer(call: types.CallbackQuery, user_id: str = None) -> None:
    """Обработка ответов
    """
    hse_user_id = call.message.chat.id if call else user_id
    logger.debug(f'{hse_user_id = }')
    logger.debug(f'{call.data = }')

    if not await check_user_access(chat_id=hse_user_id):
        logger.error(f'access fail {hse_user_id = }')
        return

    # prefix: str = spotter_data.get('calld_prefix', None)
    # if prefix is None:
    #     logger.error(f'{prefix}')
    #     return
    #
    # table_name: str = spotter_data.get('character_table_name', None)
    # if table_name is None:
    #     logger.error(f'Item {table_name} is None. return')
    #     return
    #
    # user_id: str = spotter_data.get('hse_user_id', None)
    # if user_id is None:
    #     logger.error(f'{user_id}')
    #     return
    #
    # item_number: str = spotter_data.get('item_number_text', None)
    # if item_number is None:
    #     logger.error(f'{item_number}')
    #     return
    #
    # character: str = spotter_data.get('character', None)
    # if character is None:
    #     logger.error(f'{character}')
    #     return

    if not await check_spotter_data():
        return

    item_number: str = spotter_data.get('item_number_text', None)
    character: str = spotter_data.get('character', None)

    # query_kwargs: dict = {
    #     "action": 'SELECT', "subject": '*',
    #     "conditions": {
    #         "id": item_number,
    #     },
    # }
    # query: str = await QueryConstructor(None, 'core_violations', **query_kwargs).prepare_data()
    #
    # violations_dataframe: DataFrame = await create_lite_dataframe_from_query(query=query, table_name='core_violations')
    # if violations_dataframe is None:
    #     text_violations: str = 'Незакрытых записей вне актов не обнаружено!'
    #     await bot_send_message(chat_id=hse_user_id, text=text_violations)
    #     return
    #
    # if violations_dataframe.empty:
    #     logger.error(f'{hse_user_id = } {Messages.Error.dataframe_is_empty}  \n{query = }')
    #     return

    violations_dataframe = await get_violations_df(item_number)

    if not await check_dataframe(violations_dataframe, hse_user_id):
        return

    type_character = await determine_type_characteristic(character)

    if type_character == 'other_meaning':
        await bot_send_message(chat_id=hse_user_id, text=Messages.Error.error_action)

    if type_character == 'complex_meaning':
        result = await complex_meaning_handler(hse_user_id, character, item_number, violations_dataframe)

    if type_character == 'simple_meaning':
        result = await simple_meaning_handler(hse_user_id, character, item_number, violations_dataframe)

    if type_character == 'text_meaning':
        result = await text_meaning_handler(hse_user_id, character, item_number, violations_dataframe)

    msg_id = call.message.message_id
    await bot_delete_message(chat_id=hse_user_id, message_id=msg_id, sleep_sec=15)


async def get_violations_df(item_number: str | int):
    """

    :return:
    """
    query_kwargs: dict = {
        "action": 'SELECT', "subject": '*',
        "conditions": {
            "id": str(item_number),
        },
    }
    query: str = await QueryConstructor(None, 'core_violations', **query_kwargs).prepare_data()

    violations_dataframe: DataFrame = await create_lite_dataframe_from_query(query=query, table_name='core_violations')
    # if violations_dataframe is None:
    #     text_violations: str = 'Незакрытых записей вне актов не обнаружено!'
    #     await bot_send_message(chat_id=hse_user_id, text=text_violations)
    #     return
    #
    # if violations_dataframe.empty:
    #     logger.error(f'{hse_user_id = } {Messages.Error.dataframe_is_empty}  \n{query = }')
    #     return

    return violations_dataframe


async def determine_type_characteristic(characteristic) -> str:
    """

    :return:
    """
    type_char = ''

    if characteristic in ['normative_documents_id', 'sub_location_id']:
        type_char = 'complex_meaning'

    if characteristic in ['comment', 'description']:
        type_char = 'text_meaning'

    if characteristic in ['title', 'file_id', 'is_published', 'violation_id']:
        type_char = 'other_meaning'

    if characteristic not in ['normative_documents_id', 'sub_location_id']:
        type_char = 'simple_meaning'

    return type_char


async def complex_meaning_handler(hse_user_id, character, item_number, violations_dataframe):
    """

    :return:
    """

    if character not in violations_dataframe.columns.values.tolist():
        return

    item_value = 1
    result_update_db: bool = await update_column_value_in_db(
        item_number=item_number, column_name=character, item_value=item_value, hse_user_id=hse_user_id
    )

    result_update_local: bool = await update_column_value_in_local(
        item_number=item_number, column_name=character, item_value=item_value, hse_user_id=hse_user_id
    )

    result_update_google: bool = await update_column_value_in_google_disk(
        item_number=item_number, column_name=character, item_value=item_value, hse_user_id=hse_user_id
    )

    spotter_data.clear()

    result_list: list = [result_update_db, result_update_local, result_update_google]

    if not all(result_list):
        await bot_send_message(
            chat_id=hse_user_id,
            text=f'{hse_user_id = } Ошибка обновления данных {item_number} {character = }!')
        return False

    await bot_send_message(
        chat_id=hse_user_id,
        text=f'{hse_user_id = } Данные записи {item_number} {character = } успешно обновлены')
    return True


async def simple_meaning_handler(hse_user_id, character, item_number, violations_dataframe):
    """

    :return:
    """

    if character not in violations_dataframe.columns.values.tolist():
        return

    item_value = 1
    result_update_db: bool = await update_column_value_in_db(
        item_number=item_number, column_name=character, item_value=item_value, hse_user_id=hse_user_id
    )

    result_update_local: bool = await update_column_value_in_local(
        item_number=item_number, column_name=character, item_value=item_value, hse_user_id=hse_user_id
    )

    result_update_google: bool = await update_column_value_in_google_disk(
        item_number=item_number, column_name=character, item_value=item_value, hse_user_id=hse_user_id
    )

    spotter_data.clear()

    result_list: list = [result_update_db, result_update_local, result_update_google]

    if not all(result_list):
        await bot_send_message(
            chat_id=hse_user_id,
            text=f'{hse_user_id = } Ошибка обновления данных {item_number} {character = }!')
        return False

    await bot_send_message(
        chat_id=hse_user_id,
        text=f'{hse_user_id = } Данные записи {item_number} {character = } успешно обновлены')
    return True


async def text_meaning_handler(hse_user_id, character, item_number, violations_dataframe):
    """

    :return:
    """

    return True
