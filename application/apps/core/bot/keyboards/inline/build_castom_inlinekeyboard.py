from loader import logger

logger.debug(f"{__name__} start import")
from aiogram import types
from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup)
from aiogram.utils.callback_data import CallbackData
from apps.core.bot.data import board_config
from apps.MyBot import MyBot

logger.debug(f"{__name__} finish import")

NUM_COL = 2
STEP_MENU = 10
move_action: CallbackData = CallbackData("description", "action", "previous_value")
posts_cb: CallbackData = CallbackData('post', 'id', 'action')


async def build_inlinekeyboard(*, some_list: list, num_col: int = 1, level: int = 1, step: int = None,
                               called_prefix: str = '', addition: list = None, previous_level: str = None,
                               postfix: str = '') -> InlineKeyboardMarkup:
    """Создание кнопок в чате для пользователя на основе some_list.
    Количество кнопок = количество элементов в списке some_list
    Расположение в n_cols столбцов
    Текст на кнопках text=ss
    Возвращаемое значение, при нажатии кнопки в чате callback_data=ss
    """
    button_list: list = []

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
        logger.debug(f'len(some_list) <= STEP_MENU {len(some_list) <= STEP_MENU}')

        button_list = button_list + [
            InlineKeyboardButton(text=ss, callback_data=f'{called_prefix}{ss}{postfix}') for ss in some_list
        ]
        menu = await _build_menu(buttons=button_list, n_cols=num_col)

        reply_markup = InlineKeyboardMarkup(resize_keyboard=True, inline_keyboard=menu)
        if previous_level:
            reply_markup = await add_previous_paragraph_button(reply_markup=reply_markup,
                                                               previous_level=previous_level)
        return reply_markup

    if STEP_MENU < len(some_list):
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


async def add_previous_paragraph_button(reply_markup, previous_level: str) -> InlineKeyboardMarkup:
    """Добавление кнопки - предыдущее действий"""

    logger.debug(f"{reply_markup = }")
    logger.debug(f"{previous_level = }")

    btn_previous = InlineKeyboardButton(text="previous",
                                        callback_data=move_action.new(
                                            action="previous_paragraph",
                                            previous_value=previous_level
                                        )
                                        )
    reply_markup.row(btn_previous)

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


@MyBot.dp.callback_query_handler(move_action.filter(action=["move_down", "move_up"]))
async def build_inlinekeyboard_answer(call: types.CallbackQuery, callback_data: dict):
    """Обработка ответа клавиш переключения уровня меню в inlinekeyboard в сообщении

    :param call:
    :param callback_data:
    :return:
    """
    menu_level = board_config.menu_level
    some_list = board_config.menu_list
    count_col = board_config.count_col
    call_fanc_name = board_config.call_fanc_name
    prefix = ''

    if call_fanc_name == 'enable_features':
        prefix = 'features_'

    chat_id = call.message.chat.id
    message_id = call.message.message_id

    if callback_data['action'] == "move_down":
        board_config.menu_level = menu_level = menu_level - 1

    if callback_data['action'] == "move_up":
        board_config.menu_level = menu_level = menu_level + 1

    reply_markup = await build_inlinekeyboard(
        some_list=some_list, num_col=count_col, level=menu_level, called_prefix=prefix
    )

    if board_config.previous_level:
        reply_markup = await add_previous_paragraph_button(reply_markup=reply_markup,
                                                           previous_level=board_config.previous_level)

    await MyBot.bot.edit_message_reply_markup(chat_id=chat_id, message_id=message_id, reply_markup=reply_markup)

    board_config.call_fanc_name = ''


async def add_subtract_inline_keyboard_with_action():
    """Формирование сообщения с текстом и кнопками действий в зависимости от параметров

    :return:
    """

    markup = types.InlineKeyboardMarkup()

    markup.add(types.InlineKeyboardButton('Корректировать значения',
                                          callback_data=posts_cb.new(id='-', action='correct_current_post')))
    markup.add(types.InlineKeyboardButton('Удалить Полностью',
                                          callback_data=posts_cb.new(id='-', action='del_current_post')))
    markup.add(types.InlineKeyboardButton('Оставить без изменений',
                                          callback_data=posts_cb.new(id='-', action='correct_abort_current_post')))

    return markup
