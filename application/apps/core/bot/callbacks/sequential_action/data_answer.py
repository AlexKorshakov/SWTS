from __future__ import annotations
from loader import logger

logger.debug(f"{__name__} start import")

import traceback
from aiogram import types
from aiogram.dispatcher import FSMContext

from apps.MyBot import bot_send_message
from apps.core.database.transformation_category import CATEGORY_ID_TRANSFORM
from apps.core.bot.data.board_config import BoardConfig as board_config
from apps.core.bot.callbacks.sequential_action.category import (get_data_list)
from apps.core.bot.keyboards.inline.build_castom_inlinekeyboard import (build_inlinekeyboard,
                                                                        build_text_for_inlinekeyboard)
from apps.core.bot.reports.report_data import ViolationData

logger.debug(f"{__name__} finish import")


async def get_and_send_start_location_data(call: types.CallbackQuery, callback_data: dict = None,
                                           user_id: int | str = None, state: FSMContext = None) -> bool:
    """Получение данных main_locations

    :param state:
    :param user_id: id пользователя
    :param callback_data:
    :param call:
    :return: bool
    """
    hse_user_id = call.message.chat.id if call else user_id

    call_func, result = await get_part_name(await fanc_name())
    this_level_name = CATEGORY_ID_TRANSFORM[call_func]
    print(f"{__name__} {result=} {await get_level_characteristics(this_level_name)}")
    await notify_user_for_choice(call, data_answer=call.data)

    previous_level = this_level_name['previous_level']

    menu_list = await get_data_list(this_level_name['this_level'])
    menu_level = await board_config(state, "menu_level", 1).set_data(call_func=await fanc_name())
    menu_list = await board_config(state, "menu_list", menu_list).set_data(call_func=await fanc_name())
    count_col = await board_config(state, "count_col", 1).set_data(call_func=await fanc_name())

    previous_level = await board_config(state, "previous_level", previous_level).set_data(call_func=await fanc_name())

    text_list: list = [this_level_name['this_level_message']]
    await board_config(state, "menu_text_list", text_list).set_data(call_func=await fanc_name())

    reply_markup = await build_inlinekeyboard(
        some_list=menu_list, num_col=count_col, level=menu_level,
        # previous_level=previous_level, use_search=True,
        state=state
    )

    text = f"{this_level_name['this_level_message']}"
    await bot_send_message(chat_id=hse_user_id, text=text, reply_markup=reply_markup)
    return True


async def get_and_send_location_data(call: types.CallbackQuery, user_id: int | str = None,
                                     state: FSMContext = None) -> bool:
    """Получение данных main_locations

    :param state:
    :param user_id: id пользователя
    :param call:
    :return: bool
    """
    hse_user_id = call.message.chat.id if call else user_id

    call_func, result = await get_part_name(await fanc_name())
    this_level_name = CATEGORY_ID_TRANSFORM[call_func]
    print(f"{__name__} {result=} {await get_level_characteristics(this_level_name)}")
    await notify_user_for_choice(call, data_answer=call.data)

    previous_level = this_level_name['previous_level']

    menu_list = await get_data_list(this_level_name['next_level'])
    menu_level = await board_config(state, "menu_level", 1).set_data(call_func=await fanc_name())
    menu_list = await board_config(state, "menu_list", menu_list).set_data(call_func=await fanc_name())
    count_col = await board_config(state, "count_col", 1).set_data(call_func=await fanc_name())

    await board_config(state, "previous_level", previous_level).set_data(call_func=await fanc_name())

    text_list: list = [this_level_name['next_level_message']]
    await board_config(state, "menu_text_list", text_list).set_data(call_func=await fanc_name())

    reply_markup = await build_inlinekeyboard(
        some_list=menu_list, num_col=count_col, level=menu_level, previous_level=previous_level, use_search=True,
        state=state
    )

    text = f"{this_level_name['next_level_message']}"
    await bot_send_message(chat_id=hse_user_id, text=text, reply_markup=reply_markup)
    return True


async def get_and_send_main_location_data(call: types.CallbackQuery, user_id: int | str = None,
                                          state: FSMContext = None) -> bool:
    """Получение данных main_locations

    :param state:
    :param user_id: id пользователя
    :param call:
    :return: bool
    """
    hse_user_id = call.message.chat.id if call else user_id

    call_func, result = await get_part_name(await fanc_name())
    this_level_name = CATEGORY_ID_TRANSFORM[call_func]
    print(f"{__name__} {result=} {await get_level_characteristics(this_level_name)}")
    await notify_user_for_choice(call, data_answer=call.data)

    previous_level = this_level_name['previous_level']

    menu_list = await get_data_list(this_level_name['next_level'])
    menu_level = await board_config(state, "menu_level", 1).set_data(call_func=await fanc_name())
    menu_list = await board_config(state, "menu_list", menu_list).set_data(call_func=await fanc_name())
    count_col = await board_config(state, "count_col", 1).set_data(call_func=await fanc_name())

    await board_config(state, "previous_level", ).set_data(previous_level, call_func=await fanc_name())

    text_list: list = [this_level_name['next_level_message']]
    await board_config(state, "menu_text_list", text_list).set_data(call_func=await fanc_name())

    reply_markup = await build_inlinekeyboard(
        some_list=menu_list, num_col=count_col, level=menu_level, previous_level=previous_level, use_search=True,
        state=state
    )

    text = f"{this_level_name['next_level_message']}"
    await bot_send_message(chat_id=hse_user_id, text=text, reply_markup=reply_markup)
    return True


async def get_and_send_main_location_data(call: types.CallbackQuery, user_id: int | str = None,
                                          state: FSMContext = None) -> bool:
    """Получение данных main_locations

    :param state:
    :param user_id: id пользователя
    :param call:
    :return: bool
    """
    hse_user_id = call.message.chat.id if call else user_id

    call_func, result = await get_part_name(await fanc_name())
    this_level_name = CATEGORY_ID_TRANSFORM[call_func]
    print(f"{__name__} {result=} {await get_level_characteristics(this_level_name)}")
    await notify_user_for_choice(call, data_answer=call.data)

    previous_level = this_level_name['previous_level']
    next_level = this_level_name['next_level']
    v_data: dict = await state.get_data()

    menu_list = await get_data_list(next_level,
                                    category=v_data[this_level_name['item']],
                                    condition='short_title'
                                    )
    logger.debug(f'{menu_list = }')
    data_list = await get_data_list(next_level,
                                    category=v_data[this_level_name['item']],
                                    condition='data_list'
                                    )

    menu_level = await board_config(state, "menu_level", 1).set_data(call_func=await fanc_name())
    menu_list = await board_config(state, "menu_list", menu_list).set_data(call_func=await fanc_name())
    count_col = await board_config(state, "count_col", 2).set_data(call_func=await fanc_name())
    await board_config(state, "previous_level", previous_level).set_data(call_func=await fanc_name())

    zipped_list: list = list(zip(menu_list, data_list))
    text_list: list = [f"{await get_character_text(item)}" for item in zipped_list]
    menu_text_list = await board_config(state, "menu_text_list", text_list).set_data(call_func=await fanc_name())

    reply_markup = await build_inlinekeyboard(
        some_list=menu_list, num_col=count_col, level=menu_level, previous_level=previous_level, use_search=True,
        state=state
    )
    reply_text = await build_text_for_inlinekeyboard(
        some_list=menu_text_list, level=menu_level
    )

    text = f"{this_level_name['next_level_message']}\n\n{reply_text}"
    await bot_send_message(chat_id=hse_user_id, text=text, reply_markup=reply_markup)
    return True


async def get_and_send_null_sub_locations_data(call: types.CallbackQuery, user_id: int | str = None,
                                               state: FSMContext = None) -> bool:
    """Получение данных sub_location

    :param state:
    :param user_id: id пользователя
    :param call:
    :return: bool
    """
    hse_user_id = call.message.chat.id if call else user_id

    call_func, result = await get_part_name(await fanc_name())
    this_level_name = CATEGORY_ID_TRANSFORM[call_func]
    print(f"{__name__} {result=} {await get_level_characteristics(this_level_name)}")

    previous_level = this_level_name['previous_level']
    next_level = this_level_name['next_level']

    await notify_user_for_choice(call, data_answer=call.data)

    menu_list = await get_data_list(next_level)
    menu_level = await board_config(state, "menu_level", 1).set_data(call_func=await fanc_name())
    menu_list = await board_config(state, "menu_list", menu_list).set_data(call_func=await fanc_name())
    text_list: list = [this_level_name['next_level_message']]
    await board_config(state, "menu_text_list", text_list).set_data(call_func=await fanc_name())
    count_col = await board_config(state, "count_col", 2).set_data(call_func=await fanc_name())
    await board_config(state, "previous_level", previous_level).set_data(call_func=await fanc_name())

    reply_markup = await build_inlinekeyboard(
        some_list=menu_list, num_col=count_col, level=menu_level, previous_level=previous_level, use_search=True,
        state=state
    )

    text = f"{this_level_name['next_level_message']}"
    await bot_send_message(chat_id=hse_user_id, text=text, reply_markup=reply_markup)
    return True


async def get_and_send_sub_locations_data(call: types.CallbackQuery, user_id: int | str = None,
                                          state: FSMContext = None) -> bool:
    """Получение данных sub_location

    :param state:
    :param user_id: id пользователя
    :param call:
    :return: bool
    """
    hse_user_id = call.message.chat.id if call else user_id

    call_func, result = await get_part_name(await fanc_name())
    this_level_name = CATEGORY_ID_TRANSFORM[call_func]
    print(f"{__name__} {result=} {await get_level_characteristics(this_level_name)}")

    previous_level = this_level_name['previous_level']
    next_level = this_level_name['next_level']

    await notify_user_for_choice(call, data_answer=call.data)

    menu_list = await get_data_list(next_level)
    menu_level = await board_config(state, "menu_level", 1).set_data(call_func=await fanc_name())
    menu_list = await board_config(state, "menu_list", menu_list).set_data(call_func=await fanc_name())
    text_list: list = [this_level_name['next_level_message']]
    await board_config(state, "menu_text_list", text_list).set_data(call_func=await fanc_name())
    count_col = await board_config(state, "count_col", 2).set_data(call_func=await fanc_name())
    await board_config(state, "previous_level", previous_level).set_data(call_func=await fanc_name())

    reply_markup = await build_inlinekeyboard(
        some_list=menu_list, num_col=count_col, level=menu_level, previous_level=previous_level, use_search=True,
        state=state
    )

    text = f"{this_level_name['next_level_message']}"
    await bot_send_message(chat_id=hse_user_id, text=text, reply_markup=reply_markup)
    return True


async def get_and_send_main_category_data(call: types.CallbackQuery, user_id: int | str = None,
                                          state: FSMContext = None) -> bool:
    """Получение данных sub_location

    :param state:
    :param user_id: id пользователя
    :param call:
    :return: bool
    """
    hse_user_id = call.message.chat.id if call else user_id

    call_func, result = await get_part_name(await fanc_name())
    this_level_name = CATEGORY_ID_TRANSFORM[call_func]
    print(f"{__name__} {result=} {await get_level_characteristics(this_level_name)}")

    previous_level = this_level_name['previous_level']
    next_level = this_level_name['next_level']

    await notify_user_for_choice(call, data_answer=call.data)

    menu_list = await get_data_list(next_level)
    menu_level = await board_config(state, "menu_level", 1).set_data(call_func=await fanc_name())
    menu_list = await board_config(state, "menu_list", menu_list).set_data(call_func=await fanc_name())
    text_list: list = [this_level_name['next_level_message']]
    await board_config(state, "menu_text_list", text_list).set_data(call_func=await fanc_name())
    count_col = await board_config(state, "count_col", 1).set_data(call_func=await fanc_name())
    await board_config(state, "previous_level", previous_level).set_data(call_func=await fanc_name())

    reply_markup = await build_inlinekeyboard(
        some_list=menu_list, num_col=count_col, level=menu_level, previous_level=previous_level, use_search=True,
        state=state
    )

    text = f"{this_level_name['next_level_message']}"
    await bot_send_message(chat_id=hse_user_id, text=text, reply_markup=reply_markup)
    return True


async def get_and_send_category_data(call: types.CallbackQuery, user_id: int | str = None,
                                     state: FSMContext = None) -> bool:
    """ Получение данных category

    :param state:
    :param user_id: id пользователя
    :param call:
    :return: bool
    """
    hse_user_id = call.message.chat.id if call else user_id

    call_func, result = await get_part_name(await fanc_name())
    this_level_name = CATEGORY_ID_TRANSFORM[call_func]
    print(f"{__name__} {result=} {await get_level_characteristics(this_level_name)}")

    previous_level = this_level_name['previous_level']
    next_level = this_level_name['next_level']

    await notify_user_for_choice(call, data_answer=call.data)

    v_data: dict = await state.get_data()

    menu_list = await get_data_list(next_level,
                                    category=v_data[this_level_name['item']],
                                    condition='short_title'
                                    )
    data_list = await get_data_list(next_level,
                                    category=v_data[this_level_name['item']],
                                    condition='data_list'
                                    )

    menu_level = await board_config(state, "menu_level", 1).set_data(call_func=await fanc_name())
    menu_list = await board_config(state, "menu_list", menu_list).set_data(call_func=await fanc_name())
    count_col = await board_config(state, "count_col", 2).set_data(call_func=await fanc_name())
    await board_config(state, "previous_level", previous_level).set_data(call_func=await fanc_name())

    zipped_list: list = list(zip(menu_list, data_list))

    text_list: list = [f"{await get_character_text(item)}" for item in zipped_list]
    menu_text_list = await board_config(state, "menu_text_list", text_list).set_data(call_func=await fanc_name())

    reply_markup = await build_inlinekeyboard(
        some_list=menu_list, num_col=count_col, level=menu_level, previous_level=previous_level, use_search=True,
        state=state
    )
    reply_text = await build_text_for_inlinekeyboard(
        some_list=menu_text_list, level=menu_level
    )

    text = f"{this_level_name['next_level_message']}\n\n{reply_text}"
    await bot_send_message(chat_id=hse_user_id, text=text, reply_markup=reply_markup)
    return True


async def get_and_send_null_normative_documents_data(call: types.CallbackQuery, user_id: int | str = None,
                                                     state: FSMContext = None) -> bool:
    """ Получение данных normative_documents

    :param state:
    :param user_id: id пользователя
    :param call:
    :return: bool
    """
    hse_user_id = call.message.chat.id if call else user_id

    call_func, result = await get_part_name(await fanc_name())
    this_level_name = CATEGORY_ID_TRANSFORM[call_func]
    print(f"{__name__} {result=} {await get_level_characteristics(this_level_name)}")

    previous_level = this_level_name['previous_level']
    next_level = this_level_name['next_level']

    await notify_user_for_choice(call, data_answer=call.data)

    menu_list = await get_data_list(next_level)
    menu_level = await board_config(state, "menu_level", 1).set_data(call_func=await fanc_name())
    menu_list = await board_config(state, "menu_list", menu_list).set_data(call_func=await fanc_name())
    text_list: list = [this_level_name['next_level_message']]
    await board_config(state, "menu_text_list", text_list).set_data(call_func=await fanc_name())
    count_col = await board_config(state, "count_col", 2).set_data(call_func=await fanc_name())
    await board_config(state, "previous_level", previous_level).set_data(call_func=await fanc_name())

    reply_markup = await build_inlinekeyboard(
        some_list=menu_list, num_col=count_col, level=menu_level, previous_level=previous_level, use_search=True,
        state=state
    )

    text = f"{this_level_name['next_level_message']}"
    await bot_send_message(chat_id=hse_user_id, text=text, reply_markup=reply_markup)
    return True


async def get_and_send_normative_documents_data(call: types.CallbackQuery, user_id: int | str = None,
                                                state: FSMContext = None) -> bool:
    """ Получение данных normative_documents

    :param state:
    :param user_id: id пользователя
    :param call:
    :return: bool
    """
    hse_user_id = call.message.chat.id if call else user_id

    call_func, result = await get_part_name(await fanc_name())
    this_level_name = CATEGORY_ID_TRANSFORM[call_func]
    print(f"{__name__} {result=} {await get_level_characteristics(this_level_name)}")

    previous_level = this_level_name['previous_level']
    next_level = this_level_name['next_level']

    await notify_user_for_choice(call, data_answer=call.data)

    menu_list = await get_data_list(next_level)
    menu_level = await board_config(state, "menu_level", 1).set_data(call_func=await fanc_name())
    menu_list = await board_config(state, "menu_list", menu_list).set_data(call_func=await fanc_name())
    text_list: list = [this_level_name['next_level_message']]
    await board_config(state, "menu_text_list", text_list).set_data(call_func=await fanc_name())
    count_col = await board_config(state, "count_col", 2).set_data(call_func=await fanc_name())
    await board_config(state, "previous_level", previous_level).set_data(call_func=await fanc_name())

    reply_markup = await build_inlinekeyboard(
        some_list=menu_list, num_col=count_col, level=menu_level, previous_level=previous_level, use_search=True,
        state=state
    )

    text = f"{this_level_name['next_level_message']}"
    await bot_send_message(chat_id=hse_user_id, text=text, reply_markup=reply_markup)
    return True


async def get_and_send_violation_category_data(call: types.CallbackQuery, user_id: int | str = None,
                                               state: FSMContext = None) -> bool:
    """Получение данных violation_category

    :param state:
    :param user_id: id пользователя
    :param call:
    :return: bool
    """
    hse_user_id = call.message.chat.id if call else user_id

    call_func, result = await get_part_name(await fanc_name())
    this_level_name = CATEGORY_ID_TRANSFORM[call_func]
    print(f"{__name__} {result=} {await get_level_characteristics(this_level_name)}")

    previous_level = this_level_name['previous_level']
    next_level = this_level_name['next_level']

    await notify_user_for_choice(call, data_answer=call.data)

    menu_list = await get_data_list(next_level)
    menu_level = await board_config(state, "menu_level", 1).set_data(call_func=await fanc_name())
    menu_list = await board_config(state, "menu_list", menu_list).set_data(call_func=await fanc_name())
    count_col = await board_config(state, "count_col", 1).set_data(call_func=await fanc_name())
    await board_config(state, "previous_level", previous_level).set_data(call_func=await fanc_name())

    text_list: list = [this_level_name['this_level_message']]
    await board_config(state, "menu_text_list", text_list).set_data(call_func=await fanc_name())

    await board_config(state, "previous_level", previous_level).set_data(call_func=await fanc_name())

    reply_markup = await build_inlinekeyboard(
        some_list=menu_list, num_col=count_col, level=menu_level, previous_level=previous_level, use_search=True,
        state=state
    )

    text = f"{this_level_name['next_level_message']}"
    await bot_send_message(chat_id=hse_user_id, text=text, reply_markup=reply_markup)
    return True


async def get_and_send_general_contractor_data(call: types.CallbackQuery, user_id: int | str = None,
                                               state: FSMContext = None) -> bool:
    """Получение данных general_contractor

    :param state:
    :param user_id: id пользователя
    :param call:
    :return: bool
    """
    hse_user_id = call.message.chat.id if call else user_id

    call_func, result = await get_part_name(await fanc_name())
    this_level_name = CATEGORY_ID_TRANSFORM[call_func]
    print(f"{__name__} {result=} {await get_level_characteristics(this_level_name)}")

    previous_level = this_level_name['previous_level']
    next_level = this_level_name['next_level']

    await notify_user_for_choice(call, data_answer=call.data)

    menu_list = await get_data_list(next_level)
    menu_level = await board_config(state, "menu_level", 1).set_data(call_func=await fanc_name())
    menu_list = await board_config(state, "menu_list", menu_list).set_data(call_func=await fanc_name())
    text_list: list = [this_level_name['next_level_message']]
    await board_config(state, "menu_text_list", text_list).set_data(call_func=await fanc_name())
    count_col = await board_config(state, "count_col", 1).set_data(call_func=await fanc_name())
    await board_config(state, "previous_level", previous_level).set_data(call_func=await fanc_name())

    reply_markup = await build_inlinekeyboard(
        some_list=menu_list, num_col=count_col, level=menu_level, previous_level=previous_level, use_search=True,
        state=state
    )

    text = f"{this_level_name['next_level_message']}"
    await bot_send_message(chat_id=hse_user_id, text=text, reply_markup=reply_markup)
    return True


async def get_and_send_incident_level_data(call: types.CallbackQuery, user_id: int | str = None,
                                           state: FSMContext = None) -> bool:
    """Получение данных incident_level

    :param state:
    :param user_id: id пользователя
    :param call:
    :return: bool
    """
    hse_user_id = call.message.chat.id if call else user_id

    call_func, result = await get_part_name(await fanc_name())
    this_level_name = CATEGORY_ID_TRANSFORM[call_func]
    print(f"{__name__} {result=} {await get_level_characteristics(this_level_name)}")

    previous_level = this_level_name['previous_level']
    next_level = this_level_name['next_level']

    await notify_user_for_choice(call, data_answer=call.data)

    menu_list = await get_data_list(next_level)
    menu_level = await board_config(state, "menu_level", 1).set_data(call_func=await fanc_name())
    menu_list = await board_config(state, "menu_list", menu_list).set_data(call_func=await fanc_name())
    text_list: list = [this_level_name['next_level_message']]
    await board_config(state, "menu_text_list", text_list).set_data(call_func=await fanc_name())
    count_col = await board_config(state, "count_col", 1).set_data(call_func=await fanc_name())
    await board_config(state, "previous_level", previous_level).set_data(call_func=await fanc_name())

    reply_markup = await build_inlinekeyboard(
        some_list=menu_list, num_col=count_col, level=menu_level, previous_level=previous_level, use_search=True,
        state=state
    )

    text = f"{this_level_name['next_level_message']}"
    await bot_send_message(chat_id=hse_user_id, text=text, reply_markup=reply_markup)
    return True


async def get_and_send_act_required_data(call: types.CallbackQuery, user_id: int | str = None,
                                         state: FSMContext = None) -> bool:
    """Получение данных act_required

    :param state:
    :param user_id: id пользователя
    :param call:
    :return: bool
    """
    hse_user_id = call.message.chat.id if call else user_id

    call_func, result = await get_part_name(await fanc_name())
    this_level_name = CATEGORY_ID_TRANSFORM[call_func]
    print(f"{__name__} {result=} {await get_level_characteristics(this_level_name)}")

    previous_level = this_level_name['previous_level']
    next_level = this_level_name['next_level']

    await notify_user_for_choice(call, data_answer=call.data)

    menu_list = await get_data_list(next_level)
    menu_level = await board_config(state, "menu_level", 1).set_data(call_func=await fanc_name())
    menu_list = await board_config(state, "menu_list", menu_list).set_data(call_func=await fanc_name())
    text_list: list = [this_level_name['next_level_message']]
    await board_config(state, "menu_text_list", text_list).set_data(call_func=await fanc_name())
    count_col = await board_config(state, "count_col", 2).set_data(call_func=await fanc_name())
    await board_config(state, "previous_level", previous_level).set_data(call_func=await fanc_name())

    reply_markup = await build_inlinekeyboard(
        some_list=menu_list, num_col=count_col, level=menu_level, previous_level=previous_level, use_search=True,
        state=state
    )

    text = f"{this_level_name['next_level_message']}"
    await bot_send_message(chat_id=hse_user_id, text=text, reply_markup=reply_markup)
    return True


async def get_and_send_elimination_time_data(call: types.CallbackQuery, user_id: int | str = None,
                                             state: FSMContext = None) -> bool:
    """Получение данных elimination_time

    :param state:
    :param user_id: id пользователя
    :param call:
    :return: bool
    """
    hse_user_id = call.message.chat.id if call else user_id

    call_func, result = await get_part_name(await fanc_name())
    this_level_name = CATEGORY_ID_TRANSFORM[call_func]
    print(f"{__name__} {result=} {await get_level_characteristics(this_level_name)}")

    previous_level = this_level_name['previous_level']
    await board_config(state, "previous_level", previous_level).set_data(call_func=await fanc_name())

    await notify_user_for_choice(call, data_answer=call.data)

    text = f"{this_level_name['next_level_message']}"
    await bot_send_message(chat_id=hse_user_id, text=text)

    # Вызов состояния ожидания текстового ответа от пользователя
    await ViolationData.description.set()
    return True


async def get_level_characteristics(level: dict) -> str:
    """Получение характеристик текущего уровня"""
    this_level_number = level.get('this_level_number')
    this_level = level.get('this_level')
    item = level.get('item')

    list_characteristics = [
        f'{item = }' if item else 'item is None',
        f'{this_level = }' if this_level else 'this_level is None',
        f'{this_level_number = }' if this_level_number else 'this_level_number is None',
    ]

    text: str = ": ".join([item for item in list_characteristics if item])
    return text


async def get_part_name(func_n: str) -> (str, bool):
    """Получение имени параметра из имени вызываемой функции func_n.
    Возвращает имя параметра func_n str и результат проверки в CATEGORY_ID_TRANSFORM bool

    :param func_n: имя вызываемой функции
    :return: str, bool
    """
    if not isinstance(func_n, str):
        return func_n

    replace_list: list = ['get_and_send_', '_data', '_null', 'start_']
    for i in replace_list:
        func_n = func_n.replace(i, '')

    result = CATEGORY_ID_TRANSFORM.get(func_n)
    return func_n, bool(result)


async def notify_user_for_choice(call_msg: types.CallbackQuery | types.Message, user_id: int | str = None,
                                 data_answer: str = None) -> bool:
    """Уведомление пользователя о выборе + логирование

    :param data_answer:
    :param user_id: int | str id пользователя
    :param call_msg:
    :return result: bool :
    """

    if isinstance(call_msg, types.CallbackQuery):
        result: bool = await is_callbackquery(call_msg, data_answer, user_id)
        return result

    if isinstance(call_msg, types.Message):
        result: bool = await is_message(call_msg, data_answer, user_id)
        return result


async def is_callbackquery(callbackquery: types.CallbackQuery, data_answer: str, user_id: int | str = None) -> bool:
    """Изменение сообщения types.CallbackQuery
    """
    for i in ('previous_paragraph', 'move_up', 'move_down'):
        if i in callbackquery.data: return True

    mesg_text: str = f"Выбрано: {data_answer}"
    if callbackquery.data in callbackquery.message.text:
        mesg_list: list = [item for item in callbackquery.message.text.split('\n\n') if callbackquery.data in item]
        mesg_text = f"Выбрано: {mesg_list[0]}"

    try:
        hse_user_id = callbackquery.message.chat.id if callbackquery else user_id
        logger.debug(f"{hse_user_id = } Выбрано: {data_answer} {callbackquery.data}")
        await callbackquery.message.edit_text(text=mesg_text, reply_markup=None)
        return True

    except Exception as err:
        logger.debug(f"{callbackquery.message.chat.id = } {repr(err)}")
        return False


async def is_message(message: types.Message, data_answer: str, user_id: int | str = None) -> bool:
    """Изменение сообщения types.Message
    """
    for i in ('previous_paragraph', 'move_up', 'move_down'):
        if i in message.text: return True

    mesg_text: str = f"Выбрано: {data_answer}"
    if message.text:
        mesg_list: list = [item for item in message.text.split('\n\n') if message.text in item]
        mesg_text = f"Выбрано: {mesg_list[0] if mesg_list else ''}"

    hse_user_id = message.chat.id if message else user_id
    logger.debug(f"{hse_user_id = } Выбрано: {data_answer} {message.text}")

    try:
        await message.edit_text(text=mesg_text, reply_markup=None)
        return True

    except Exception as err:
        logger.debug(f"{message.chat.id = } {repr(err)}")
        return False


async def get_character_text(param_list: list | str) -> list | str:
    """

    :return:
    """
    if isinstance(param_list, list):
        if not param_list: return []
        text_list: list = [
            f"item {item.get('id')} {item.get('title')} " for item in param_list if item.get('id') is not None
        ]
        return text_list

    if isinstance(param_list, dict):
        if not param_list: return ''
        text_list: str = f"item {param_list.get('id')} {param_list.get('title')} {param_list.get('comment')} "
        return text_list

    if isinstance(param_list, tuple):
        if not param_list: return ''
        text_list: str = f"{param_list[0]} : {param_list[1]}"
        return text_list


async def fanc_name() -> str:
    """Возвращает имя вызываемой функции"""
    stack = traceback.extract_stack()
    return str(stack[-2][2])
