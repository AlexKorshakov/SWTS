from __future__ import annotations

import math

from loader import logger

logger.debug(f"{__name__} start import")
from aiogram import types
from aiogram.dispatcher import FSMContext
from apps.MyBot import bot_send_message
from apps.core.bot.data.board_config import BoardConfig as board_config
from apps.core.bot.callbacks.sequential_action.category import get_data_list
from apps.core.bot.keyboards.inline.build_castom_inlinekeyboard import build_inlinekeyboard, \
    build_text_for_inlinekeyboard
from apps.core.bot.messages.messages import Messages
from apps.core.bot.reports.report_data import ViolationData

logger.debug(f"{__name__} finish import")


async def get_and_send_start_main_locations_data(
        call: types.CallbackQuery, callback_data: dict = None, user_id: int | str = None, state: FSMContext = None,
        data_answer: str = None
) -> bool:
    """Получение данных main_locations

    :param data_answer:
    :param state:
    :param user_id: id пользователя
    :param callback_data:
    :param call:
    :return: bool
    """
    hse_user_id = call.message.chat.id if call else user_id
    this_level = 'main_locations'.upper()

    await notify_user_for_choice(call, data_answer=data_answer if data_answer else '')

    # menu_level = board_config.menu_level = 1
    # menu_list = board_config.menu_list = get_data_list(this_level)
    # count_col = board_config.count_col = 1
    # board_config.previous_level = ''

    menu_level = await board_config(state, "menu_level", 1).set_data()
    menu_list = await board_config(state, "menu_list", get_data_list(this_level)).set_data()
    menu_text_list = await board_config(state, "menu_text_list", [Messages.Choose.main_category]).set_data()
    count_col = await board_config(state, "count_col", 1).set_data()
    await board_config(state, "previous_level", '').set_data()

    reply_markup = await build_inlinekeyboard(some_list=menu_list, num_col=count_col, level=menu_level, state=state)

    await bot_send_message(
        chat_id=hse_user_id, text=Messages.Choose.main_category, reply_markup=reply_markup
    )

    return True


async def get_and_send_main_locations_data(call: types.CallbackQuery, callback_data: dict = None,
                                           user_id: int | str = None, state: FSMContext = None) -> bool:
    """Получение данных main_locations

    :param state:
    :param user_id: id пользователя
    :param callback_data:
    :param call:
    :return: bool
    """
    hse_user_id = call.message.chat.id if call else user_id

    previous_level = 'main_locations'
    this_level = 'main_locations'
    next_level = 'sub_locations'.upper()

    await notify_user_for_choice(call, data_answer=call.data)

    v_data: dict = await state.get_data()

    short_title = get_data_list(next_level,
                                category=v_data["main_location"],
                                condition='short_title'
                                )

    logger.debug(f'{short_title = }')

    data_list = get_data_list(next_level,
                              category=v_data["main_location"],
                              condition='data_list'
                              )
    # menu_level = board_config.menu_level = 1
    # menu_list = board_config.menu_list = short_title
    # count_col = board_config.count_col = 2
    # board_config.previous_level = previous_level

    menu_level = await board_config(state, "menu_level", 1).set_data()
    menu_list = await board_config(state, "menu_list", short_title).set_data()
    count_col = await board_config(state, "count_col", 2).set_data()
    await board_config(state, "previous_level", previous_level).set_data()

    zipped_list: list = list(zip(short_title, data_list))

    # text_items: str = get_text(datas=zipped_list)
    # for item_txt in text_processor(text_items):
    #     await bot_send_message(chat_id=hse_user_id, text=item_txt)

    text_list: list = [f"{await get_character_text(item)}" for item in zipped_list if item[0][0] != '#']

    # menu_text_list = board_config.menu_text_list = text_list
    menu_text_list = await board_config(state, "menu_text_list", text_list).set_data()

    # text_list = await text_process(zipped_list)
    #
    # for txt in text_list:
    #     await bot_send_message(chat_id=hse_user_id,
    #                            text=txt)

    reply_markup = await build_inlinekeyboard(
        some_list=menu_list, num_col=count_col, level=menu_level, previous_level=previous_level, use_search=True,
        state=state
    )

    reply_text = await build_text_for_inlinekeyboard(
        some_list=menu_text_list, level=menu_level, use_search=True
    )
    text = f'{Messages.Choose.sub_location}\n\n{reply_text}'

    await bot_send_message(chat_id=hse_user_id, text=text, reply_markup=reply_markup)
    return True


async def get_and_send_null_sub_locations_data(call: types.CallbackQuery, callback_data: dict = None,
                                               user_id: int | str = None, state: FSMContext = None) -> bool:
    """Получение данных sub_location

    :param state:
    :param user_id: id пользователя
    :param callback_data:
    :param call:
    :return: bool
    """
    hse_user_id = call.message.chat.id if call else user_id
    previous_level: str = 'main_locations'
    this_level: str = 'sub_locations'
    next_level: str = 'main_category'.upper()

    await notify_user_for_choice(call, data_answer=call.data)

    # menu_level = board_config.menu_level = 1
    # menu_list = board_config.menu_list = get_data_list(next_level)
    # count_col = board_config.count_col = 2
    # board_config.previous_level = previous_level

    menu_level = await board_config(state, "menu_level", 1).set_data()
    menu_list = await board_config(state, "menu_list", get_data_list(next_level)).set_data()
    menu_text_list = await board_config(state, "menu_text_list", [Messages.Choose.main_category]).set_data()
    count_col = await board_config(state, "count_col", 2).set_data()
    await board_config(state, "previous_level", previous_level).set_data()

    reply_markup = await build_inlinekeyboard(
        some_list=menu_list, num_col=count_col, level=menu_level, previous_level=previous_level, use_search=True,
        state=state
    )
    await bot_send_message(chat_id=hse_user_id, text=Messages.Choose.main_category, reply_markup=reply_markup)
    return True


async def get_and_send_sub_locations_data(call: types.CallbackQuery, callback_data: dict = None,
                                          user_id: int | str = None, state: FSMContext = None) -> bool:
    """Получение данных sub_location

    :param state:
    :param user_id: id пользователя
    :param callback_data:
    :param call:
    :return: bool
    """
    hse_user_id = call.message.chat.id if call else user_id
    previous_level: str = 'main_locations'
    this_level: str = 'sub_locations'
    next_level: str = 'main_category'.upper()

    await notify_user_for_choice(call, data_answer=call.data)

    # menu_level = board_config.menu_level = 1
    # menu_list = board_config.menu_list = get_data_list(next_level)
    # count_col = board_config.count_col = 2
    # board_config.previous_level = previous_level

    menu_level = await board_config(state, "menu_level", 1).set_data()
    menu_list = await board_config(state, "menu_list", get_data_list(next_level)).set_data()
    menu_text_list = await board_config(state, "menu_text_list", [Messages.Choose.main_category]).set_data()
    count_col = await board_config(state, "count_col", 2).set_data()
    await board_config(state, "previous_level", previous_level).set_data()

    reply_markup = await build_inlinekeyboard(
        some_list=menu_list, num_col=count_col, level=menu_level, previous_level=previous_level, use_search=True,
        state=state
    )
    await bot_send_message(chat_id=hse_user_id, text=Messages.Choose.main_category, reply_markup=reply_markup)
    return True


async def get_and_send_main_category_data(call: types.CallbackQuery, callback_data: dict = None,
                                          user_id: int | str = None, state: FSMContext = None) -> bool:
    """Получение данных sub_location

    :param state:
    :param user_id: id пользователя
    :param callback_data:
    :param call:
    :return: bool
    """
    hse_user_id = call.message.chat.id if call else user_id
    previous_level: str = 'main_locations'
    this_level: str = 'main_category'
    next_level: str = 'category'.upper()

    await notify_user_for_choice(call, data_answer=call.data)

    # menu_level = board_config.menu_level = 1
    # menu_list = board_config.menu_list = get_data_list(next_level)
    # count_col = board_config.count_col = 1
    # board_config.previous_level = previous_level

    menu_level = await board_config(state, "menu_level", 1).set_data()
    menu_list = await board_config(state, "menu_list", get_data_list(next_level)).set_data()
    menu_text_list = await board_config(state, "menu_text_list", [Messages.Choose.category]).set_data()
    count_col = await board_config(state, "count_col", 1).set_data()
    await board_config(state, "previous_level", previous_level).set_data()

    reply_markup = await build_inlinekeyboard(
        some_list=menu_list, num_col=count_col, level=menu_level, previous_level=previous_level, state=state
    )
    await bot_send_message(chat_id=hse_user_id, text=Messages.Choose.category, reply_markup=reply_markup)
    return True


async def get_and_send_category_data(call: types.CallbackQuery, callback_data: dict = None,
                                     user_id: int | str = None, state: FSMContext = None) -> bool:
    """ Получение данных category

    :param state:
    :param user_id: id пользователя
    :param call:
    :param callback_data:
    :return: bool
    """
    hse_user_id = call.message.chat.id if call else user_id
    previous_level: str = 'main_category'
    this_level: str = 'category'
    next_level: str = 'normative_documents'.upper()

    await notify_user_for_choice(call, data_answer=call.data)

    v_data: dict = await state.get_data()

    short_title = get_data_list(next_level,
                                category=v_data["category"],
                                condition='short_title'
                                )
    data_list = get_data_list(next_level,
                              category=v_data["category"],
                              condition='data_list'
                              )
    # menu_level = board_config.menu_level = 1
    # menu_list = board_config.menu_list = short_title
    # count_col = board_config.count_col = 2
    # board_config.previous_level = previous_level

    menu_level = await board_config(state, "menu_level", 1).set_data()
    menu_list = await board_config(state, "menu_list", short_title).set_data()
    count_col = await board_config(state, "count_col", 2).set_data()
    await board_config(state, "previous_level", previous_level).set_data()

    zipped_list: list = list(zip(short_title, data_list))
    # text_items: str = get_text(datas=zipped_list)
    # for item_txt in text_processor(text_items):
    #     await bot_send_message(chat_id=hse_user_id, text=item_txt)

    text_list: list = [f"{await get_character_text(item)}" for item in zipped_list if item[0][0] != '#']

    # menu_text_list = board_config.menu_text_list = text_list
    menu_text_list = await board_config(state, "menu_text_list", text_list).set_data()

    # text_list = await text_process(zipped_list)
    #
    # for txt in text_list:
    #     await bot_send_message(chat_id=hse_user_id,
    #                            text=txt)

    reply_markup = await build_inlinekeyboard(
        some_list=menu_list, num_col=count_col, level=menu_level, previous_level=previous_level, use_search=True,
        state=state
    )
    reply_text = await build_text_for_inlinekeyboard(
        some_list=menu_text_list, level=menu_level, use_search=True
    )

    text = f'{Messages.Choose.normative_documents}\n\n{reply_text}'

    await bot_send_message(chat_id=hse_user_id, text=text, reply_markup=reply_markup)
    return True


async def get_and_send_null_normative_documents_data(call: types.CallbackQuery, callback_data: dict = None,
                                                     user_id: int | str = None, state: FSMContext = None) -> bool:
    """ Получение данных normative_documents

    :param state:
    :param user_id: id пользователя
    :param call:
    :param callback_data:
    :return: bool
    """
    hse_user_id = call.message.chat.id if call else user_id
    previous_level: str = 'category'
    this_level: str = 'normative_documents'
    next_level: str = 'violation_category'.upper()

    await notify_user_for_choice(call, data_answer=call.data)

    # menu_level = board_config.menu_level = 1
    # menu_list = board_config.menu_list = get_data_list(next_level)
    # count_col = board_config.count_col = 2
    # board_config.previous_level = previous_level

    menu_level = await board_config(state, "menu_level", 1).set_data()
    menu_list = await board_config(state, "menu_list", get_data_list(next_level)).set_data()
    menu_text_list = await board_config(state, "menu_text_list", [Messages.Choose.violation_category]).set_data()
    count_col = await board_config(state, "count_col", 2).set_data()
    await board_config(state, "previous_level", previous_level).set_data()

    reply_markup = await build_inlinekeyboard(
        some_list=menu_list, num_col=count_col, level=menu_level, previous_level=previous_level, use_search=True,
        state=state
    )
    await bot_send_message(chat_id=hse_user_id, text=Messages.Choose.violation_category, reply_markup=reply_markup)
    return True


async def get_and_send_normative_documents_data(call: types.CallbackQuery, callback_data: dict = None,
                                                user_id: int | str = None, state: FSMContext = None) -> bool:
    """ Получение данных normative_documents

    :param state:
    :param user_id: id пользователя
    :param call:
    :param callback_data:
    :return: bool
    """
    hse_user_id = call.message.chat.id if call else user_id
    previous_level: str = 'category'
    this_level: str = 'normative_documents'
    next_level: str = 'violation_category'.upper()

    await notify_user_for_choice(call, data_answer=call.data)

    # menu_level = board_config.menu_level = 1
    # menu_list = board_config.menu_list = get_data_list(next_level)
    # count_col = board_config.count_col = 2
    # board_config.previous_level = previous_level

    menu_level = await board_config(state, "menu_level", 1).set_data()
    menu_list = await board_config(state, "menu_list", get_data_list(next_level)).set_data()
    menu_text_list = await board_config(state, "menu_text_list", [Messages.Choose.category]).set_data()
    count_col = await board_config(state, "count_col", 2).set_data()
    await board_config(state, "previous_level", previous_level).set_data()

    reply_markup = await build_inlinekeyboard(
        some_list=menu_list, num_col=count_col, level=menu_level, previous_level=previous_level, use_search=True,
        state=state
    )
    await bot_send_message(chat_id=hse_user_id, text=Messages.Choose.category, reply_markup=reply_markup)
    return True


async def get_and_send_violation_category_data(call: types.CallbackQuery, callback_data: dict = None,
                                               user_id: int | str = None, state: FSMContext = None) -> bool:
    """Получение данных violation_category

    :param state:
    :param user_id: id пользователя
    :param call:
    :param callback_data:
    :return: bool
    """
    hse_user_id = call.message.chat.id if call else user_id
    previous_level: str = 'category'
    this_level: str = 'violation_category'
    next_level: str = 'general_contractors'.upper()

    await notify_user_for_choice(call, data_answer=call.data)

    # menu_level = board_config.menu_level = 1
    # menu_list = board_config.menu_list = get_data_list(next_level)
    # # count_col = board_config.count_col = 1
    # board_config.previous_level = previous_level

    menu_level = await board_config(state, "menu_level", 1).set_data()
    menu_list = await board_config(state, "menu_list", get_data_list(next_level)).set_data()
    # count_col = await board_config(state, "count_col", 1).set_data()
    await board_config(state, "previous_level", previous_level).set_data()

    # reply_markup = await build_inlinekeyboard(
    #     some_list=menu_list, num_col=count_col, level=menu_level, previous_level=previous_level, state= state
    # )
    # await bot_send_message(chat_id=hse_user_id,
    #                        text=Messages.Choose.general_constractor, reply_markup=reply_markup)
    # return True

    # v_data: dict = await state.get_data()
    short_title = get_data_list(next_level,
                                # category=v_data["category"],
                                # condition='short_title'
                                )
    data_list = get_data_list(next_level,
                              # category=v_data["category"],
                              # condition='data_list'
                              )

    zipped_list: list = list(zip(short_title, data_list))

    text_list: list = [f"{await get_character_text(item)}" for item in zipped_list if item[0][0] != '#']

    # menu_text_list = board_config.menu_text_list = text_list
    # count_col = board_config.count_col = 1
    # board_config.previous_level = previous_level
    menu_text_list = await board_config(state, "menu_text_list", text_list).set_data()
    count_col = await board_config(state, "count_col", 1).set_data()
    await board_config(state, "previous_level", previous_level).set_data()

    reply_markup = await build_inlinekeyboard(
        some_list=menu_list, num_col=count_col, level=menu_level, previous_level=previous_level, use_search=True,
        state=state
    )

    reply_text = await build_text_for_inlinekeyboard(
        some_list=menu_text_list, level=menu_level,
        use_search=True
    )

    text = f'{Messages.Choose.general_constractor}\n\n{reply_text}'

    await bot_send_message(chat_id=hse_user_id, text=text, reply_markup=reply_markup)
    return True


async def get_and_send_general_contractors_data(call: types.CallbackQuery, callback_data: dict = None,
                                                user_id: int | str = None, state: FSMContext = None) -> bool:
    """Получение данных general_contractors

    :param state:
    :param user_id: id пользователя
    :param call:
    :param callback_data:
    :return: bool
    """
    hse_user_id = call.message.chat.id if call else user_id
    previous_level: str = 'violation_category'
    this_level: str = 'general_contractors'
    next_level: str = 'incident_level'.upper()

    await notify_user_for_choice(call, data_answer=call.data)

    # menu_level = board_config.menu_level = 1
    # menu_list = board_config.menu_list = get_data_list(next_level)
    # count_col = board_config.count_col = 1
    # board_config.previous_level = previous_level

    menu_level = await board_config(state, "menu_level", 1).set_data()
    menu_list = await board_config(state, "menu_list", get_data_list(next_level)).set_data()
    menu_text_list = await board_config(state, "menu_text_list", [Messages.Choose.incident_level]).set_data()
    count_col = await board_config(state, "count_col", 1).set_data()
    await board_config(state, "previous_level", previous_level).set_data()

    reply_markup = await build_inlinekeyboard(
        some_list=menu_list, num_col=count_col, level=menu_level, previous_level=previous_level, use_search=True,
        state=state
    )
    await bot_send_message(chat_id=hse_user_id, text=Messages.Choose.incident_level, reply_markup=reply_markup)
    return True


async def get_and_send_incident_level_data(call: types.CallbackQuery, callback_data: dict = None,
                                           user_id: int | str = None, state: FSMContext = None) -> bool:
    """Получение данных incident_level

    :param state:
    :param user_id: id пользователя
    :param call:
    :param callback_data:
    :return: bool
    """
    hse_user_id = call.message.chat.id if call else user_id
    previous_level: str = 'general_contractors'
    this_level: str = 'incident_level'
    next_level: str = 'act_required'.upper()

    await notify_user_for_choice(call, data_answer=call.data)

    # menu_level = board_config.menu_level = 1
    # menu_list = board_config.menu_list = get_data_list(next_level)
    # count_col = board_config.count_col = 1
    # board_config.previous_level = previous_level

    menu_level = await board_config(state, "menu_level", 1).set_data()
    menu_list = await board_config(state, "menu_list", get_data_list(next_level)).set_data()
    menu_text_list = await board_config(state, "menu_text_list", [Messages.Choose.act_required]).set_data()
    count_col = await board_config(state, "count_col", 1).set_data()
    await board_config(state, "previous_level", previous_level).set_data()

    reply_markup = await build_inlinekeyboard(
        some_list=menu_list, num_col=count_col, level=menu_level, previous_level=previous_level, state=state
    )
    await bot_send_message(chat_id=hse_user_id, text=Messages.Choose.act_required, reply_markup=reply_markup)
    return True


async def get_and_send_act_required_data(call: types.CallbackQuery, callback_data: dict = None,
                                         user_id: int | str = None, state: FSMContext = None) -> bool:
    """Получение данных act_required

    :param state:
    :param user_id: id пользователя
    :param call:
    :param callback_data:
    :return: bool
    """
    hse_user_id = call.message.chat.id if call else user_id
    previous_level: str = 'incident_level'
    this_level: str = 'act_required'
    next_level: str = 'elimination_time'.upper()

    await notify_user_for_choice(call, data_answer=call.data)

    # menu_level = board_config.menu_level = 1
    # menu_list = board_config.menu_list = get_data_list(next_level)
    # count_col = board_config.count_col = 2
    # board_config.previous_level = previous_level

    menu_level = await board_config(state, "menu_level", 1).set_data()
    menu_list = await board_config(state, "menu_list", get_data_list(next_level)).set_data()
    menu_text_list = await board_config(state, "menu_text_list", [Messages.Choose.elimination_time]).set_data()
    count_col = await board_config(state, "count_col", 2).set_data()
    await board_config(state, "previous_level", previous_level).set_data()

    reply_markup = await build_inlinekeyboard(
        some_list=menu_list, num_col=count_col, level=menu_level, previous_level=previous_level, state=state
    )
    await bot_send_message(chat_id=hse_user_id, text=Messages.Choose.elimination_time, reply_markup=reply_markup)
    return True


async def get_and_send_elimination_time_data(call: types.CallbackQuery, callback_data: dict = None,
                                             user_id: int | str = None, state: FSMContext = None) -> bool:
    """Получение данных act_required

    :param state:
    :param user_id: id пользователя
    :param call:
    :param callback_data:
    :return: bool
    """
    hse_user_id = call.message.chat.id if call else user_id
    # board_config.previous_level = ''
    await board_config(state, "previous_level", '').set_data()

    await notify_user_for_choice(call, data_answer=call.data)

    await bot_send_message(chat_id=hse_user_id, text=Messages.Enter.description_violation)

    # Вызов состояния ожидания текстового ответа от пользователя
    await ViolationData.description.set()
    return True


async def notify_user_for_choice(call: types.CallbackQuery, user_id: int | str = None, data_answer: str = None) -> bool:
    """Уведомление пользователя о выборе + логирование

    :param data_answer:
    :param user_id: int | str id пользователя
    :param call:
    :return None :
    """
    for i in ['previous_paragraph', 'move_up', 'move_down']:
        if i in call.data: return True

    mesg_text: str = f"Выбрано: {data_answer}"
    if call.data in call.message.text:
        mesg_list: list = [item for item in call.message.text.split('\n\n') if call.data in item]
        mesg_text = f"Выбрано: {mesg_list[0]}"

    try:
        hse_user_id = call.message.chat.id if call else user_id
        logger.debug(f"{hse_user_id = } Выбрано: {data_answer} {call.data}")
        await call.message.edit_text(text=mesg_text, reply_markup=None)
        return True

    except Exception as err:
        logger.debug(f"{call.message.chat.id = } {repr(err)}")


def get_text(datas: list) -> str:
    """

    :return:
    """

    short_title_list: list = [str(item[0]) for item in datas]
    title_data_list: list = [item[1] for item in datas]
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

# async def text_process(zipped_list: list) -> list:
#     """Формирование тела сообщения
#
#     :param zipped_list:
#     :return: bool
#     """
#
#     text = '\n\n'.join(str(item[0]) + " : " + str(item[1]) for item in zipped_list)
#
#     if len(text) <= 3500:
#         return [text]
#
#     text = ''
#     text_list = []
#     for item in zipped_list:
#         if item[0][0] == '#': continue
#
#         text = text + f' \n\n {str(item[0])} : {str(item[1])}'
#         if len(text) > 3500:
#             text_list.append(text)
#             text = ''
#
#     return text_list


# async def test():
#     previous_level: str = 'main_category'
#     this_level: str = 'category'
#     next_level: str = 'normative_documents'.upper()
#
#     short_title = get_data_list(next_level,
#                                 category='ТС/Спецтехника',
#                                 condition='short_title'
#                                 )
#     data_list = get_data_list(next_level,
#                               category='ТС/Спецтехника',
#                               condition='data_list'
#                               )
#
#     menu_level = await board_config(state, "menu_level", 1).set_data()
#     menu_list = await board_config(state, "menu_list", short_title).set_data()
#     count_col = await board_config(state, "count_col", 2).set_data()
#     await board_config(state, "previous_level", previous_level).set_data()
#     await board_config(state, "this_level", this_level).set_data()
#
#     zipped_list: list = list(zip(short_title, data_list))
#
#     # text_list = await text_process(zipped_list)
#     #
#     # for txt in text_list:
#     #     print(txt)
#     # await bot_send_message(text=txt)
#
#     reply_markup = await build_inlinekeyboard(
#         some_list=menu_list, num_col=count_col, level=menu_level, previous_level=previous_level, state= state
#     )
#     print(reply_markup)
#
#
# if __name__ == '__main__':
#     asyncio.run(test())
