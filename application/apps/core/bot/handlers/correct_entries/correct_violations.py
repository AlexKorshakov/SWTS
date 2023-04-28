from __future__ import annotations

from aiogram import types
from pandas import DataFrame

from apps.MyBot import MyBot, bot_send_message, bot_delete_message
from apps.core.bot.bot_utils.check_user_registration import check_user_access
from apps.core.bot.data import board_config
from apps.core.bot.handlers.correct_entries.correct_acts import call_correct_acts
from apps.core.bot.handlers.correct_entries.correct_non_act_item_item_correct import \
    RESULT_DICT, create_lite_dataframe_from_query, COLUMNS_DICT
from apps.core.bot.handlers.correct_entries.correct_support_updater import update_column_value_in_db, \
    update_column_value_in_local, update_column_value_in_google_disk
from apps.core.bot.handlers.correct_entries.correct_support import spotter_data, get_item_number_from_call, \
    check_dataframe, check_spotter_data, get_violations_df
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

        if 'title' not in table_dataframe.columns.values.tolist():
            return

        title_list: list = table_dataframe['id'].tolist()
        title_list: list = [f"item_{item}" for item in title_list if item is not None]

        menu_level = board_config.menu_level = 1
        count_col = board_config.count_col = 1

        reply_markup = await build_inlinekeyboard(
            some_list=title_list, num_col=count_col, level=menu_level, calld_prefix=f"corr_{character_table_name}_"
        )

        character_text: str = await text_processor_character_text(table_dataframe, character, item_number_text)

        await bot_send_message(
            chat_id=hse_user_id, text=character_text, reply_markup=reply_markup
        )

        spotter_data['calld_prefix'] = f"corr_{character_table_name}_"
        spotter_data['character_table_name'] = f"{character_table_name}"
        spotter_data['hse_user_id'] = f"{hse_user_id}"
        spotter_data['item_number_text'] = f"{item_number_text}"
        spotter_data['character'] = f"{character}"

    # await bot_send_message(chat_id=hse_user_id, text=Messages.Error.error_action)

    msg_id = call.message.message_id
    await bot_delete_message(chat_id=hse_user_id, message_id=msg_id, sleep_sec=15)


async def text_processor_character_text(table_dataframe: DataFrame, character: str,
                                        item_number_text: str | int) -> str:
    """Формирование текста для отправки пользователю

    """

    unique_items_ids: list = table_dataframe.id.unique().tolist()
    unique_items_titles: list = table_dataframe.title.unique().tolist()

    items_text_list: list = []
    for i, (item_id, item_title) in enumerate(zip(unique_items_ids, unique_items_titles), 1):
        item_info: str = f'item_{item_id} : {item_title}'
        items_text_list.append(item_info)
        logger.debug(f'{i} :: {item_info}')

    items_text: str = '\n'.join(items_text_list)

    character_title: str = COLUMNS_DICT.get(character, None)

    header_text: str = f'Выберите значение для показателя Изменить "{character_title}" для ' \
                       f'записи item_number_{item_number_text}'
    footer_text: str = 'Нажмите на кнопку с номером выбранного значения'

    final_text: str = f'{header_text} \n\n{items_text}  \n\n{footer_text}'

    return final_text


@MyBot.dp.callback_query_handler(lambda call: 'characteristic_' in call.data)
async def call_characteristic_answer(call: types.CallbackQuery, user_id: str = None) -> None:
    """Обработка ответов
    """
    characteristic_text = call.data

    hse_user_id = call.message.chat.id if call else user_id
    logger.info(f'{hse_user_id = } {call.data = }')

    text_violations = f'Выбрано {characteristic_text}'

    reply_markup = await add_act_inline_keyboard_with_action()

    await bot_send_message(chat_id=hse_user_id, text=text_violations, reply_markup=reply_markup)

    msg_id = call.message.message_id
    await bot_delete_message(chat_id=hse_user_id, message_id=msg_id, sleep_sec=15)


@MyBot.dp.callback_query_handler(lambda call: 'corr_' in call.data)
async def call_correct_item_answer(call: types.CallbackQuery, user_id: str | int = None):
    """Обработка ответов
    """
    hse_user_id = call.message.chat.id if call else user_id
    logger.debug(f'{hse_user_id = }')
    logger.debug(f'{call.data = }')

    if not await check_user_access(chat_id=hse_user_id):
        logger.error(f'access fail {hse_user_id = }')
        return

    if not await check_spotter_data():
        return

    item_number: str = spotter_data.get('item_number_text', None)
    character: str = spotter_data.get('character', None)
    character_id: str = call.data.split('_')[-1]

    violations_dataframe = await get_violations_df(item_number, hse_user_id)

    if not await check_dataframe(violations_dataframe, hse_user_id):
        return

    type_character = await determine_type_characteristic(character)

    if type_character == 'other_meaning':
        await bot_send_message(chat_id=hse_user_id, text=Messages.Error.error_action)

    elif type_character == 'complex_meaning':
        result = await complex_meaning_handler(hse_user_id, character, item_number, violations_dataframe)

    elif type_character == 'simple_meaning':
        result = await simple_meaning_handler(hse_user_id, character, character_id, item_number, violations_dataframe)

    elif type_character == 'text_meaning':
        result = await text_meaning_handler(hse_user_id, character, item_number, violations_dataframe)

    await call_correct_acts(user_id=hse_user_id)

    msg_id = call.message.message_id
    await bot_delete_message(chat_id=hse_user_id, message_id=msg_id, sleep_sec=15)


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


async def simple_meaning_handler(hse_user_id, character, character_id, item_number, violations_dataframe):
    """

    :return:
    """

    if character not in violations_dataframe.columns.values.tolist():
        return

    result_update_db: bool = await update_column_value_in_db(
        item_number=item_number, column_name=character, item_value=character_id, hse_user_id=hse_user_id
    )

    result_update_local: bool = await update_column_value_in_local(
        item_number=item_number, column_name=character, item_value=character_id,
        hse_user_id=hse_user_id, v_df=violations_dataframe
    )

    result_update_google: bool = await update_column_value_in_google_disk(
        item_number=item_number, column_name=character, item_value=character_id, hse_user_id=hse_user_id
    )

    spotter_data.clear()

    result_list: list = [result_update_db, result_update_local, result_update_google]

    if not all(result_list):
        await bot_send_message(
            chat_id=hse_user_id,
            text=f'{hse_user_id = } Ошибка обновления данных {item_number} {character = }!'
        )
        return False

    await bot_send_message(
        chat_id=hse_user_id,
        text=f'{hse_user_id = } Данные записи {item_number} {character = } успешно обновлены'
    )
    return True


async def text_meaning_handler(hse_user_id, character, item_number, violations_dataframe):
    """

    :return:
    """

    return True


async def add_act_inline_keyboard_with_action():
    """Формирование сообщения с текстом и кнопками действий в зависимости от параметров

    :return:
    """
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('Изменить значение',
                                          callback_data=posts_cb.new(id='-', action='correct_character')))
    markup.add(types.InlineKeyboardButton('Отмена',
                                          callback_data=posts_cb.new(id='-', action='correct_characteristic_not')))
    return markup
