# import asyncio

from aiogram import types

from apps.core.bot.data import board_config
from apps.core.bot.data.category import get_data_list
from apps.core.bot.keyboards.inline.build_castom_inlinekeyboard import build_inlinekeyboard
from apps.core.bot.messages.messages import Messages
from apps.core.bot.reports.report_data import violation_data
from apps.core.bot.states import AnswerUserState
from loader import logger


async def get_and_send_start_main_locations_data(call: types.CallbackQuery, callback_data: dict = None):
    """Получение данных main_locations

    :param callback_data:
    :param call:
    :return:
    """

    this_level = 'main_locations'.upper()

    await notify_user_for_choice(call, callback_data, level=this_level)

    menu_level = board_config.menu_level = 1
    menu_list = board_config.menu_list = get_data_list(this_level)
    count_col = board_config.count_col = 1
    board_config.previous_level = ''

    reply_markup = await build_inlinekeyboard(some_list=menu_list, num_col=count_col, level=menu_level)

    await call.message.answer(text=Messages.Choose.main_category, reply_markup=reply_markup)


async def get_and_send_main_locations_data(call: types.CallbackQuery, callback_data: dict = None):
    """Получение данных main_locations

    :param callback_data:
    :param call:
    :return:
    """
    previous_level = 'main_locations'
    this_level = 'main_locations'
    next_level = 'sub_locations'.upper()

    await notify_user_for_choice(call, callback_data, level=this_level)

    short_title = get_data_list(next_level,
                                category=violation_data["main_location"],
                                condition='short_title'
                                )

    print(f'{short_title = }')

    data_list = get_data_list(next_level,
                              category=violation_data["main_location"],
                              condition='data_list'
                              )
    menu_level = board_config.menu_level = 1
    menu_list = board_config.menu_list = short_title
    count_col = board_config.count_col = 2
    board_config.previous_level = previous_level

    zipped_list: list = list(zip(short_title, data_list))

    text = f'{Messages.Choose.sub_location} \n\n' + \
           ' \n\n'.join(str(item[0]) + " : " + str(item[1]) for item in zipped_list)

    reply_markup = await build_inlinekeyboard(some_list=menu_list, num_col=count_col, level=menu_level,
                                              previous_level=previous_level)

    await call.message.answer(text=text, reply_markup=reply_markup)


async def get_and_send_null_sub_locations_data(call: types.CallbackQuery, callback_data: dict = None):
    """Получение данных sub_location

    :param callback_data:
    :param call:
    :return:
    """
    previous_level = 'main_locations'
    this_level = 'sub_locations'
    next_level = 'main_category'.upper()

    await notify_user_for_choice(call, callback_data, level=this_level)

    menu_level = board_config.menu_level = 1
    menu_list = board_config.menu_list = get_data_list(next_level)
    count_col = board_config.count_col = 2
    board_config.previous_level = previous_level

    reply_markup = await build_inlinekeyboard(some_list=menu_list, num_col=count_col, level=menu_level,
                                              previous_level=previous_level)
    await call.message.answer(text=Messages.Choose.main_category, reply_markup=reply_markup)


async def get_and_send_sub_locations_data(call: types.CallbackQuery, callback_data: dict = None):
    """Получение данных sub_location

    :param callback_data:
    :param call:
    :return:
    """

    previous_level = 'main_locations'
    this_level = 'sub_locations'
    next_level = 'main_category'.upper()

    await notify_user_for_choice(call, callback_data, level=this_level)

    menu_level = board_config.menu_level = 1
    menu_list = board_config.menu_list = get_data_list(next_level)
    count_col = board_config.count_col = 2
    board_config.previous_level = previous_level

    reply_markup = await build_inlinekeyboard(some_list=menu_list, num_col=count_col, level=menu_level,
                                              previous_level=previous_level)
    await call.message.answer(text=Messages.Choose.main_category, reply_markup=reply_markup)


async def get_and_send_main_category_data(call: types.CallbackQuery, callback_data: dict = None):
    """Получение данных sub_location

    :param callback_data:
    :param call:
    :return:
    """
    previous_level = 'main_locations'
    this_level = 'main_category'
    next_level = 'category'.upper()

    await notify_user_for_choice(call, callback_data, level=this_level)

    menu_level = board_config.menu_level = 1
    menu_list = board_config.menu_list = get_data_list(next_level)
    count_col = board_config.count_col = 1
    board_config.previous_level = previous_level

    reply_markup = await build_inlinekeyboard(some_list=menu_list, num_col=count_col, level=menu_level,
                                              previous_level=previous_level)
    await call.message.answer(text=Messages.Choose.category, reply_markup=reply_markup)


async def get_and_send_category_data(call: types.CallbackQuery, callback_data: dict = None):
    """ Получение данных category

    :param call:
    :param callback_data:
    :return:
    """
    previous_level = 'main_category'
    this_level = 'category'
    next_level = 'normative_documents'.upper()

    await notify_user_for_choice(call, callback_data, level=this_level)

    short_title = get_data_list(next_level,
                                category=violation_data["category"],
                                condition='short_title'
                                )
    data_list = get_data_list(next_level,
                              category=violation_data["category"],
                              condition='data_list'
                              )
    menu_level = board_config.menu_level = 1
    menu_list = board_config.menu_list = short_title
    count_col = board_config.count_col = 2
    board_config.previous_level = previous_level

    zipped_list: list = list(zip(short_title, data_list))

    text = f'{Messages.Choose.normative_documents} \n\n' + \
           ' \n\n'.join(str(item[0]) + " : " + str(item[1]) for item in zipped_list)

    reply_markup = await build_inlinekeyboard(some_list=menu_list, num_col=count_col, level=menu_level,
                                              previous_level=previous_level)
    await call.message.answer(text=text, reply_markup=reply_markup)


async def get_and_send_null_normative_documents_data(call: types.CallbackQuery, callback_data: dict = None):
    """ Получение данных normative_documents

    :param call:
    :param callback_data:
    :return:
    """
    previous_level = 'category'
    this_level = 'normative_documents'
    next_level = 'violation_category'.upper()

    await notify_user_for_choice(call, callback_data, level=this_level)

    menu_level = board_config.menu_level = 1
    menu_list = board_config.menu_list = get_data_list(next_level)
    count_col = board_config.count_col = 2
    board_config.previous_level = previous_level

    reply_markup = await build_inlinekeyboard(some_list=menu_list, num_col=count_col, level=menu_level,
                                              previous_level=previous_level)
    await call.message.answer(text=Messages.Choose.violation_category, reply_markup=reply_markup)


async def get_and_send_normative_documents_data(call: types.CallbackQuery, callback_data: dict = None):
    """ Получение данных normative_documents

    :param call:
    :param callback_data:
    :return:
    """
    previous_level = 'category'
    this_level = 'normative_documents'
    next_level = 'violation_category'.upper()

    await notify_user_for_choice(call, callback_data, level=this_level)

    menu_level = board_config.menu_level = 1
    menu_list = board_config.menu_list = get_data_list(next_level)
    count_col = board_config.count_col = 2
    board_config.previous_level = previous_level

    reply_markup = await build_inlinekeyboard(some_list=menu_list, num_col=count_col, level=menu_level,
                                              previous_level=previous_level)
    await call.message.answer(text=Messages.Choose.category, reply_markup=reply_markup)


async def get_and_send_violation_category_data(call: types.CallbackQuery, callback_data: dict = None):
    """Получение данных violation_category

    :param call:
    :param callback_data:
    :return:
    """
    previous_level = 'category'
    this_level = 'violation_category'
    next_level = 'general_contractors'.upper()

    await notify_user_for_choice(call, callback_data, level=this_level)

    menu_level = board_config.menu_level = 1
    menu_list = board_config.menu_list = get_data_list(next_level)
    count_col = board_config.count_col = 1
    board_config.previous_level = previous_level

    reply_markup = await build_inlinekeyboard(some_list=menu_list, num_col=count_col, level=menu_level,
                                              previous_level=previous_level)
    await call.message.answer(text=Messages.Choose.general_constractor, reply_markup=reply_markup)


async def get_and_send_general_contractors_data(call: types.CallbackQuery, callback_data: dict = None):
    """Получение данных general_contractors

    :param call:
    :param callback_data:
    :return:
    """
    previous_level = 'violation_category'
    this_level = 'general_contractors'
    next_level = 'incident_level'.upper()

    await notify_user_for_choice(call, callback_data, level=this_level)

    menu_level = board_config.menu_level = 1
    menu_list = board_config.menu_list = get_data_list(next_level)
    count_col = board_config.count_col = 1
    board_config.previous_level = previous_level

    reply_markup = await build_inlinekeyboard(some_list=menu_list, num_col=count_col, level=menu_level,
                                              previous_level=previous_level)
    await call.message.answer(text=Messages.Choose.incident_level, reply_markup=reply_markup)


async def get_and_send_incident_level_data(call: types.CallbackQuery, callback_data: dict = None):
    """Получение данных incident_level

    :param call:
    :param callback_data:
    :return:
    """

    previous_level = 'general_contractors'
    this_level = 'incident_level'
    next_level = 'act_required'.upper()

    await notify_user_for_choice(call, callback_data, level=this_level)

    menu_level = board_config.menu_level = 1
    menu_list = board_config.menu_list = get_data_list(next_level)
    count_col = board_config.count_col = 1
    board_config.previous_level = previous_level

    reply_markup = await build_inlinekeyboard(some_list=menu_list, num_col=count_col, level=menu_level,
                                              previous_level=previous_level)
    await call.message.answer(text=Messages.Choose.act_required, reply_markup=reply_markup)


async def get_and_send_act_required_data(call: types.CallbackQuery, callback_data: dict = None):
    """Получение данных act_required

    :param call:
    :param callback_data:
    :return:
    """
    previous_level = 'incident_level'
    this_level = 'act_required'
    next_level = 'elimination_time'.upper()

    await notify_user_for_choice(call, callback_data, level=this_level)

    menu_level = board_config.menu_level = 1
    menu_list = board_config.menu_list = get_data_list(next_level)
    count_col = board_config.count_col = 2
    board_config.previous_level = previous_level

    reply_markup = await build_inlinekeyboard(some_list=menu_list, num_col=count_col, level=menu_level,
                                              previous_level=previous_level)
    await call.message.answer(text=Messages.Choose.elimination_time, reply_markup=reply_markup)


async def get_and_send_elimination_time_data(call: types.CallbackQuery, callback_data: dict = None):
    """Получение данных act_required

    :param call:
    :param callback_data:
    :return:
    """
    board_config.previous_level = ''

    await notify_user_for_choice(call, callback_data, level='act_required')

    await call.message.answer(Messages.Enter.description_violation)

    # Вызов состояния ожидания текстового ответа от пользователя
    await AnswerUserState.description.set()


async def notify_user_for_choice(call, callback_data, level):
    """Уведомление пользователя о выборе и логирование

    :return:
    """

    await call.message.edit_reply_markup()
    await call.message.answer(text=f"Выбрано: {call.data}")
    logger.debug(f"Выбрано: {call.data}")

    if callback_data:
        logger.debug(f"Выбрано: {callback_data.get('action', None)}")
        logger.debug(f"User {call.message.chat.id} choices {callback_data.get('action', None)} {level}")
