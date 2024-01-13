from __future__ import annotations

from apps.core.bot.callbacks.sequential_action.data_answer import notify_user_for_choice
from loader import logger

logger.debug(f"{__name__} start import")
import math
import traceback

from aiogram.dispatcher import FSMContext
from aiogram import types

from apps.MyBot import MyBot, bot_send_message
from apps.core.database.query_constructor import QueryConstructor
from apps.core.database.db_utils import db_get_data_list_no_async
from apps.core.bot.data.board_config import BoardConfig as board_config
from apps.core.bot.keyboards.inline.build_castom_inlinekeyboard import (build_inlinekeyboard,
                                                                        build_text_for_inlinekeyboard)
from apps.core.bot.messages.messages import Messages
from apps.core.bot.callbacks.sequential_action.category import (_PREFIX_ND,
                                                                _PREFIX_POZ,
                                                                get_data_with_hashtags)
from apps.core.bot.reports.report_data import ViolationData

logger.debug(f"{__name__} finish import")


@MyBot.dp.callback_query_handler(lambda call: call.data[0] == '#', state=ViolationData.all_states)
async def normative_documents_answer_with_hashtags(call: types.CallbackQuery, state: FSMContext = None,
                                                   user_id: str = None) -> None:
    """Обработка ответов содержащихся в hashtags
    """

    hse_user_id = call.message.chat.id if call else user_id
    logger.info(f'{call.data = }')

    await notify_user_for_choice(call, data_answer=call.data)

    v_data: dict = await state.get_data()

    if call.data in get_data_with_hashtags("core_normativedocuments", item_id=v_data.get('category_id', None)):
        logger.info(f'{__name__} {say_fanc_name()} NORMATIVE_DOCUMENTS')
        kwargs: dict = {
            "action": 'SELECT', "subject": '*',
            "conditions": {
                "category_id": v_data.get('category_id', None),
                "hashtag": call.data,
                "hashtag_condition": 'like',
            }
        }
        query: str = await QueryConstructor(table_name='core_normativedocuments', **kwargs).prepare_data()
        # logger.info(f'{__name__} {fanc_name()} {query}')
        datas_query: list = db_get_data_list_no_async(query=query)

        previous_level = 'category'

        menu_level = await board_config(state, "menu_level", 1).set_data()
        menu_list = await board_config(state, "menu_list",
                                       [_PREFIX_ND + str(item[0]) for item in datas_query]).set_data()
        count_col = await board_config(state, "count_col", 2).set_data()
        await board_config(state, "previous_level", previous_level).set_data()

        short_title = [_PREFIX_POZ + str(item[0]) for item in datas_query]
        data_list = [str(item[2]) for item in datas_query]

        zipped_list: list = list(zip(short_title, data_list))
        # text_list: list = [f"{await get_character_text(item)}" for item in zipped_list if item[0][0] != '#']
        text_list: list = [f"{await get_character_text(item)}" for item in zipped_list]
        menu_text_list = await board_config(state, "menu_text_list", text_list).set_data()

        reply_markup = await build_inlinekeyboard(
            some_list=menu_list, num_col=count_col, level=menu_level, previous_level=previous_level, state=state
        )
        reply_text = await build_text_for_inlinekeyboard(
            some_list=menu_text_list, level=menu_level
        )

        text: str = f'{Messages.Choose.normative_documents}\n\n{reply_text}'
        await bot_send_message(chat_id=hse_user_id, text=text, reply_markup=reply_markup)
        return

    if call.data in get_data_with_hashtags("core_sublocation", item_id=v_data.get('main_location_id', None)):
        logger.info(f'{__name__} {say_fanc_name()} SUB_LOCATIONS')
        kwargs: dict = {
            "action": 'SELECT', "subject": '*',
            "conditions": {
                "main_location_id": v_data.get('main_location_id', None),
                "hashtag": call.data,
                "hashtag_condition": 'like',
            }
        }
        query: str = await QueryConstructor(table_name='core_sublocation', **kwargs).prepare_data()
        logger.info(f'{__name__} {say_fanc_name()} {query}')
        datas_query: list = db_get_data_list_no_async(query=query)

        previous_level = 'main_location'

        menu_level = await board_config(state, "menu_level", 1).set_data()
        menu_list = await board_config(state, "menu_list",
                                       [_PREFIX_POZ + str(item[0]) for item in datas_query]).set_data()
        count_col = await board_config(state, "count_col", 2).set_data()
        await board_config(state, "previous_level", previous_level).set_data()

        short_title = [_PREFIX_POZ + str(item[0]) for item in datas_query]
        data_list = [str(item[2]) for item in datas_query]

        zipped_list: list = list(zip(short_title, data_list))
        # text_list: list = [f"{await get_character_text(item)}" for item in zipped_list if item[0][0] != '#']
        text_list: list = [f"{await get_character_text(item)}" for item in zipped_list]
        menu_text_list = await board_config(state, "menu_text_list", text_list).set_data()

        reply_markup = await build_inlinekeyboard(
            some_list=menu_list, num_col=count_col, level=menu_level, previous_level=previous_level, state=state
        )
        reply_text = await build_text_for_inlinekeyboard(
            some_list=menu_text_list, level=menu_level
        )

        text: str = f'{Messages.Choose.sub_location}\n\n{reply_text}'
        await bot_send_message(chat_id=hse_user_id, text=text, reply_markup=reply_markup)
        return

    return None


async def get_character_text(param_list: list | str) -> list | str:
    """

    :return:
    """

    if isinstance(param_list, list):
        if not param_list: return []

        text_list: list = [
            f"item {item.get('id')} {item.get('title')} " \
            # f"\nvalue : {'on' if item.get('value') == 1 else 'off'}"
            for item in param_list if
            item.get('id') is not None
        ]
        return text_list

    if isinstance(param_list, dict):
        if not param_list: return ''

        text_list: str = f"item {param_list.get('id')} {param_list.get('title')} {param_list.get('comment')} " \
            # f"\nvalue : {'on' if param_list.get('value') == 1 else 'off'}"

        return text_list

    if isinstance(param_list, tuple):
        if not param_list: return ''
        if param_list[0][0] == '#': return ''

        text_list: str = f"{param_list[0]} : {param_list[1]}"

        return text_list


def get_text(prefix: str, datas: list) -> str:
    """

    :return:
    """

    short_title_list: list = [prefix + str(item[0]) for item in datas]
    title_data_list: list = [item[2] for item in datas]
    text: str = '\n\n'.join(f'{item[0]} : {item[1]}'
                            for item in
                            list(zip(short_title_list, title_data_list)))
    return text


def text_processor(text: str = None) -> list:
    """Принимает text для формирования list ответа
    Если len(text) <= 3500 - отправляет [сообщение]
    Если len(text) > 3500 - формирует list_with_parts_text = []

    :param text:
    :return: list - list_with_parts_text
    """
    if not text:
        return []

    step = 3500
    if len(text) <= step:
        return [text]

    len_parts = math.ceil(len(text) / step)
    list_with_parts_text: list = [text[step * (i - 1):step * i] for i in range(1, len_parts + 1)]

    return list_with_parts_text


def say_fanc_name():
    stack = traceback.extract_stack()
    return str(stack[-2][2])


if __name__ == '__main__':

    db_table_name = 'core_normativedocuments'
    hashtag_test = '#Огнетушители'
    query_test: str = f"SELECT * FROM {db_table_name} WHERE `category_id` == {16} AND `hashtags` LIKE '%{hashtag_test}%'"
    print(f'{__name__} {say_fanc_name()} {query_test}')

    datas_query_test: list = db_get_data_list_no_async(query=query_test)
    clean_datas_query_test: list = [item[1] for item in datas_query_test]
    short_title = [_PREFIX_ND + str(item[0]) for item in datas_query_test]

    data_list = [item[2] for item in datas_query_test]
    data_text: str = '\n\n'.join(
        f'{item[0]} : {item[1]}'
        for item in
        list(zip(short_title, data_list))
    )

    text_list: list = text_processor(data_text)

    for txt in text_list:
        print(txt)
