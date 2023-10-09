from __future__ import annotations

from apps.core.bot.data.board_config import BoardConfig as board_config
from apps.core.bot.reports.report_data import ViolationData
from loader import logger

logger.debug(f"{__name__} start import")
from pandas import DataFrame

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup)
from aiogram.utils.callback_data import CallbackData

from apps.core.bot.filters.custom_filters import is_private
from apps.MyBot import MyBot, bot_send_message

logger.debug(f"{__name__} finish import")

NUM_COL = 2
STEP_MENU = 10
move_action: CallbackData = CallbackData("description", "action", "previous_value")
posts_cb: CallbackData = CallbackData('post', 'id', 'action')


async def build_inlinekeyboard(*, some_list: list = None, num_col: int = 1, level: int = 1, step: int = None,
                               called_prefix: str = '', addition: list = None, previous_level: str = None,
                               postfix: str = '', use_search=False, state: FSMContext = None) -> InlineKeyboardMarkup:
    """Создание кнопок в чате для пользователя на основе some_list.
    Количество кнопок = количество элементов в списке some_list
    Расположение в n_cols столбцов
    Текст на кнопках text=ss
    Возвращаемое значение, при нажатии кнопки в чате callback_data=ss
    """
    button_list: list = []

    if not some_list:
        reply_markup = await add_previous_paragraph_button(previous_level=previous_level)
        return reply_markup

    some_list: list = check_list_bytes_len(some_list=some_list)

    if addition:
        button_list: list = [item for item in addition if item is not None]

    if step:
        button_list: list = button_list + [
            InlineKeyboardButton(text=ss, callback_data=f'{called_prefix}{ss}{postfix}') for ss in some_list
        ]
        menu: list = await _build_menu(buttons=button_list, n_cols=num_col)

        reply_markup = InlineKeyboardMarkup(resize_keyboard=True, inline_keyboard=menu)
        if previous_level:
            reply_markup = await add_previous_paragraph_button(
                reply_markup=reply_markup, previous_level=previous_level
            )
        return reply_markup

    if len(some_list) <= STEP_MENU:
        # board_config.use_search = False
        await board_config(state).set_data('use_search', False)

        logger.debug(f'len(some_list) <= STEP_MENU {len(some_list) <= STEP_MENU}')

        button_list = button_list + [
            InlineKeyboardButton(text=ss, callback_data=f'{called_prefix}{ss}{postfix}') for ss in some_list
        ]
        menu = await _build_menu(buttons=button_list, n_cols=num_col)

        reply_markup = InlineKeyboardMarkup(resize_keyboard=True, inline_keyboard=menu)
        if previous_level:
            reply_markup = await add_previous_paragraph_button(
                reply_markup=reply_markup, previous_level=previous_level
            )
        return reply_markup

    if len(some_list) > STEP_MENU:
        # board_config.use_search = True
        await board_config(state).set_data('use_search', True)

        logger.debug(f'STEP_MENU < len(some_list) {STEP_MENU < len(some_list)}')
        end_list: int = len(some_list)
        start_index, stop_index = await define_indices(level, end_list)

        button_list: list = button_list + [
            InlineKeyboardButton(text=ss, callback_data=f'{called_prefix}{ss}{postfix}')
            for ss in some_list[start_index:stop_index]
        ]

        menu: list = await _build_menu(buttons=button_list, n_cols=num_col)

        reply_markup = InlineKeyboardMarkup(resize_keyboard=True, inline_keyboard=menu)

        reply_markup = await add_action_button(
            reply_markup=reply_markup, start_index=start_index, stop_index=stop_index, end_list=end_list
        )

        if previous_level:
            reply_markup = await add_previous_paragraph_button(
                reply_markup=reply_markup, previous_level=previous_level
            )

        if use_search:
            reply_markup = await add_use_search_button(
                reply_markup=reply_markup, previous_level=''
            )

        return reply_markup


async def get_button_list(button_list: list, some_list: list, calld_prefix: str = '', postfix: str = '',
                          **kwargs: dict) -> list:
    """

    :return:
    """
    if not some_list:
        return button_list

    if not isinstance(some_list, list):
        return []

    button_list: list = button_list + await get_button_list_for_list(
        prefix=calld_prefix, postfix=postfix, some_list=some_list, **kwargs
    )
    return button_list


async def get_button_list_for_list(*, some_list: list, prefix: str = '', postfix: str = '', **kwargs: dict) -> list:
    """Функция формирования данных button_list с InlineKeyboardButton из some_list с использованием prefix и postfix


    :param prefix: префикс, добавляемый перед основными данными
    :param postfix: префикс, добавляемый после основных данных
    :param some_list: list с данными для формирования button_list с InlineKeyboardButton
    :param kwargs: Дополнительные параметры
    :return:
    """

    logger.info(f'{kwargs}')

    if not some_list:
        return []

    if not isinstance(some_list, list):
        return []

    for item in some_list:

        if isinstance(item, list):
            button_list: list = [
                InlineKeyboardButton(
                    text=ss,
                    callback_data=f'{prefix}{ss}{postfix}') for ss in some_list
            ]
            return button_list

        if isinstance(item, tuple):
            button_list: list = [
                InlineKeyboardButton(
                    text=ss[0],
                    callback_data=f'{prefix}{ss[1]}{postfix}') for ss in some_list
            ]
            return button_list

        if isinstance(item, dict):
            button_list: list = [
                InlineKeyboardButton(
                    text=key,
                    callback_data=f'{prefix}{val}{postfix}') for key, val in item.items()
            ]
            return button_list


def check_list_bytes_len(some_list: list) -> list:
    """Проверка длинны записи в байтах для формирования надписей кнопок
    текст длиннее 64 байт обрезается, добавляются точки
    """
    processed_values: len = []
    for item in some_list:
        if len(item.encode('utf-8')) > 62:
            logger.debug(f" {item} : {len(item.encode('utf-8'))}")

            while int(len(item.encode('utf-8'))) > 60:
                item = item[:-1]
                logger.debug(f" {item} : {len(item.encode('utf-8'))}")

            item = item[:-2] + '...'
            logger.debug(f" {item} : {len(item.encode('utf-8'))}")

        processed_values.append(item)

    return processed_values


async def check_text_bytes_len(some_text: str) -> str:
    """Проверка длинны записи в байтах для формирования надписей кнопок
    текст длиннее 64 байт обрезается, добавляются точки
    """

    if len(some_text.encode('utf-8')) > 62:
        logger.debug(f" {some_text} : {len(some_text.encode('utf-8'))}")

        while int(len(some_text.encode('utf-8'))) > 60:
            some_text = some_text[:-1]
            logger.debug(f" {some_text} : {len(some_text.encode('utf-8'))}")

        some_text = some_text[:-2] + '...'
        logger.debug(f" {some_text} : {len(some_text.encode('utf-8'))}")

    return some_text


async def define_indices(level, end_list):
    """Определение начального и конечного индекса для среза на основе level
    """
    start_index = 0 if level == 1 else (STEP_MENU * level) - STEP_MENU

    if level == 1:
        start_index = 0

    stop_index = STEP_MENU if start_index == 0 else start_index + STEP_MENU
    stop_index = end_list if stop_index > end_list else start_index + STEP_MENU

    return start_index, stop_index


async def define_max_level(menu_list: list = None):
    """Определение начального и конечного индекса для среза на основе level
    """
    if not menu_list:
        return 1, 1

    min_level = 1
    max_index = len(menu_list) // STEP_MENU
    if len(menu_list) - (STEP_MENU * max_index) != 0:
        max_index += 1

    return min_level, max_index


async def add_action_button(reply_markup, start_index: int, stop_index: int, end_list: int) -> InlineKeyboardMarkup:
    """Добавление кнопок навигации в зависимости от начального (start_index),
    конечного индекса (stop_index) и конца списка list (end_list)
    :param start_index:
    :param end_list:
    :param stop_index:
    :param reply_markup:
    :return: reply_markup
    """
    bt_down = InlineKeyboardButton(text="<--", callback_data=move_action.new(action="move_down", previous_value=''))
    bt_up = InlineKeyboardButton(text="-->", callback_data=move_action.new(action="move_up", previous_value=''))

    if start_index == 0:
        reply_markup.row(bt_up)
        # reply_markup.add(bt_up)
        return reply_markup

    if stop_index == end_list:
        reply_markup.row(bt_down)  # добавление кнопок в новую строку # ПРИОРИТЕТ
        # reply_markup.add(bt_down)  # добавление кнопок в конец списка
        return reply_markup

    reply_markup.row(bt_down, bt_up)
    # reply_markup.add(bt_down).add(bt_up)

    return reply_markup


async def add_previous_paragraph_button(reply_markup=None, previous_level: str = None) -> InlineKeyboardMarkup:
    """Добавление кнопки - предыдущее действий"""

    logger.debug(f"{reply_markup = } {previous_level = }")

    if not reply_markup:
        reply_markup = InlineKeyboardMarkup(resize_keyboard=True)

    if not previous_level:
        return reply_markup

    # previous_level: list = check_list_bytes_len(some_list=[previous_level])

    btn_previous = InlineKeyboardButton(text="previous",
                                        callback_data=move_action.new(action="previous_paragraph",
                                                                      previous_value=previous_level
                                                                      )
                                        )
    reply_markup.row(btn_previous)

    return reply_markup


async def add_use_search_button(reply_markup, previous_level: str = '') -> InlineKeyboardMarkup:
    """Добавление кнопки - предыдущее действий"""

    search_button = InlineKeyboardButton(text="поиск",
                                         callback_data=move_action.new(action="search",
                                                                       previous_value=previous_level)
                                         )
    reply_markup.inline_keyboard.insert(0, [search_button])

    return reply_markup


async def _build_menu(buttons: list, n_cols: int = 1, header_buttons: list = None, footer_buttons: list = None) -> list:
    """Создание меню кнопок
    """
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]

    if header_buttons:
        menu.insert(0, [header_buttons])
    if footer_buttons:
        menu.append([footer_buttons])
    return menu


@MyBot.dp.callback_query_handler(move_action.filter(action=["move_down", "move_up"]), state='*')
async def build_inlinekeyboard_answer(call: types.CallbackQuery, callback_data: dict, state: FSMContext = None,
                                      user_id: str | int = None):
    """Обработка ответа клавиш переключения уровня меню в inlinekeyboard в сообщении

    :param user_id:
    :param state:
    :param call:
    :param callback_data:
    :return:
    """

    hse_user_id = user_id if user_id else call.message.chat.id

    v_data: dict = await state.get_data()

    menu_level = v_data.get('menu_level')
    menu_list = v_data.get('menu_list', [])
    menu_text_list = v_data.get('menu_text_list', menu_list[0])
    use_search = v_data.get('use_search')
    count_col = v_data.get('count_col')
    call_fanc_name = v_data.get('call_fanc_name', '')

    prefix = ''

    if call_fanc_name == 'enable_features':
        prefix = 'features_'

    chat_id = call.message.chat.id
    message_id = call.message.message_id

    if callback_data['action'] == "move_down":
        # board_config(user=hse_user_id).menu_level  = menu_level - 1
        # min_level, max_index = await define_max_level(menu_list)
        menu_level = await board_config(state, "menu_level", menu_level - 1).set_data()

    if callback_data['action'] == "move_up":
        # # board_config(user=hse_user_id).menu_level  = menu_level + 1
        # min_level, max_index = await define_max_level(menu_list)
        menu_level = await board_config(state, "menu_level", menu_level + 1).set_data()

    reply_markup = await build_inlinekeyboard(
        some_list=menu_list, num_col=count_col, level=menu_level, called_prefix=prefix, use_search=use_search,
        state=state
    )

    reply_text = await build_text_for_inlinekeyboard(
        some_list=menu_text_list, level=menu_level
    )

    if v_data['previous_level']:
        reply_markup = await add_previous_paragraph_button(
            reply_markup=reply_markup, previous_level=v_data['previous_level']
        )

    await MyBot.bot.edit_message_text(
        text=reply_text, chat_id=chat_id, message_id=message_id, reply_markup=reply_markup
    )
    # await MyBot.bot.edit_message_reply_markup(chat_id=chat_id, message_id=message_id, reply_markup=reply_markup)

    # board_config(user=hse_user_id).call_fanc_name = ''
    await board_config(state, "call_fanc_name", '').set_data()


@MyBot.dp.callback_query_handler(move_action.filter(action=["search"]), state='*')
async def build_inlinekeyboard_answer(call: types.CallbackQuery, callback_data: dict, state: FSMContext = None):
    """Обработка ответа клавиш переключения уровня меню в inlinekeyboard в сообщении

    :param call:
    :param callback_data:
    :return:
    """

    item_txt: str = 'введите текстовый зарос'

    chat_id = call.message.chat.id
    message_id = call.message.message_id

    await ViolationData.inquiry.set()

    await state.update_data(chat_id=chat_id)
    await state.update_data(message_id=message_id)

    await MyBot.bot.edit_message_text(
        text=item_txt, chat_id=chat_id, message_id=message_id
    )


@MyBot.dp.message_handler(is_private, state=ViolationData.inquiry)
async def search_data_all_states_answer(message: types.Message = None, user_id: int | str = None, text: str = None,
                                        state: FSMContext = None):
    """Обработка изменений

    :param text:
    :param user_id:
    :param message:
    :param state:
    :return:
    """
    hse_user_id = user_id if user_id else message.chat.id

    # await state.finish()

    text_too_search: str = message.text if message else text

    # menu_level = board_config(user=hse_user_id).menu_level
    # menu_list = board_config(user=hse_user_id).menu_list
    # menu_text_list = board_config(user=hse_user_id).menu_text_list
    # use_search = board_config(user=hse_user_id).use_search
    # count_col = board_config(user=hse_user_id).count_col
    # call_fanc_name = board_config(user=hse_user_id).call_fanc_name
    v_data: dict = await state.get_data()

    menu_level = v_data.get('menu_level')
    menu_list = v_data.get('menu_list', [])
    menu_text_list = v_data.get('menu_text_list', menu_list[0])
    use_search = v_data.get('use_search')
    count_col = v_data.get('count_col')
    call_fanc_name = v_data.get('call_fanc_name', '')

    prefix = ''

    if call_fanc_name == 'enable_features':
        prefix = 'features_'

    chat_id: str = v_data.get('chat_id')
    message_id = v_data.get('message_id')

    # if callback_data['action'] == "search":
    #     board_config(user=hse_user_id).menu_level = menu_level = menu_level - 1
    #
    # end_list: int = len(menu_list)
    # start_index, stop_index = await define_indices(menu_level, end_list)

    menu_list = [item for item in menu_list if item[0] != '#']

    dataframe: DataFrame = await create_dataframe(menu_list, menu_text_list)

    menu_list, menu_text_list = await processor_search_if_str(
        dataframe, text_too_search=text_too_search, chat_id=str(chat_id)
    )

    reply_markup = await build_inlinekeyboard(
        some_list=menu_list, num_col=count_col, level=menu_level, called_prefix=prefix, use_search=use_search,
        state=state
    )
    reply_text = await build_text_for_inlinekeyboard(
        some_list=menu_text_list, level=menu_level
    )

    if not reply_text:
        reply_text = 'Нет данных для отображения'
        await bot_send_message(text=reply_text, chat_id=chat_id)
        # board_config(user=hse_user_id).call_fanc_name = ''
        await board_config(state, "call_fanc_name", '').set_data()

    await bot_send_message(
        text=reply_text, chat_id=chat_id, reply_markup=reply_markup
        # message_id=message_id,
    )

    # board_config(user=hse_user_id).call_fanc_name = ''
    await board_config(state, "call_fanc_name", '').set_data()


async def build_text_for_inlinekeyboard(*, some_list: list, level: int = 1, use_search=False) -> list:
    """

    :param use_search:
    :param some_list:
    :param level:
    :return:
    """

    text_list: list = []

    if len(some_list) > STEP_MENU:
        logger.debug(f'STEP_MENU < len(some_list) {STEP_MENU < len(some_list)}')
        end_list: int = len(some_list)
        start_index, stop_index = await define_indices(level, end_list)

        text_list: list = text_list + some_list[start_index:stop_index]
        text_list: str = '\n\n'.join(text_list)

        return text_list

    if len(some_list) <= STEP_MENU:
        logger.debug(f'len(some_list) <= STEP_MENU {len(some_list) <= STEP_MENU}')

        text_list = text_list + some_list
        text_list: str = '\n\n'.join(text_list)

        return text_list


async def create_dataframe(menu_list: list, menu_text_list: list) -> DataFrame:
    """

    :return:
    """
    df = None
    data_dict: dict = {'index': menu_list, 'text': menu_text_list}
    try:
        df = DataFrame(data=data_dict)

    except ValueError as err:
        logger.warning(f'Error create_dataframe {repr(err)}')

    return df


async def processor_search_if_str(table_dataframe: DataFrame, text_too_search: str, chat_id: str) -> (list, list):
    """

    :param chat_id:
    :param table_dataframe:
    :param text_too_search:
    :return:
    """

    menu_list, menu_text_list = [], []

    if not await check_dataframe(table_dataframe, chat_id):
        return [], []

    for num_col, col_item in enumerate(table_dataframe):
        if num_col == 7: break

        mask = table_dataframe[col_item].str.contains(f"{text_too_search}", case=False, regex=True, na=False)

        df_res: DataFrame = table_dataframe.loc[mask]

        menu_list = list(df_res['index'])
        menu_text_list = list(df_res['text'])

    return menu_list, menu_text_list


async def check_dataframe(dataframe: DataFrame, hse_user_id: str) -> bool:
    """Проверка dataframe на наличие данных

    :param dataframe:
    :param hse_user_id: id пользователя
    :return:
    """
    if dataframe is None:
        text_violations: str = 'не удалось получить данные!'
        # logger.error(f'{hse_user_id = } {text_violations}')
        # await bot_send_message(chat_id=hse_user_id, text=text_violations)
        return False

    if dataframe.empty:
        # logger.error(f'{hse_user_id = } {Messages.Error.dataframe_is_empty}')
        return False

    return True
