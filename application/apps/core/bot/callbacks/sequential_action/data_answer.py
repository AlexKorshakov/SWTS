from __future__ import annotations
from loader import logger

logger.debug(f"{__name__} start import")
import asyncio
from aiogram import types
from apps.MyBot import bot_send_message
from apps.core.bot.data import board_config
from apps.core.bot.data.category import get_data_list
from apps.core.bot.keyboards.inline.build_castom_inlinekeyboard import build_inlinekeyboard
from apps.core.bot.messages.messages import Messages
from apps.core.bot.reports.report_data import violation_data
from apps.core.bot.states import AnswerUserState
logger.debug(f"{__name__} finish import")


async def get_and_send_start_main_locations_data(call: types.CallbackQuery, callback_data: dict = None,
                                                 user_id: int | str = None) -> bool:
    """Получение данных main_locations

    :param user_id:
    :param callback_data:
    :param call:
    :return: bool
    """
    hse_user_id = call.message.chat.id if call else user_id
    this_level = 'main_locations'.upper()

    await notify_user_for_choice(call, callback_data, level=this_level)

    menu_level = board_config.menu_level = 1
    menu_list = board_config.menu_list = get_data_list(this_level)
    count_col = board_config.count_col = 1
    board_config.previous_level = ''

    reply_markup = await build_inlinekeyboard(some_list=menu_list, num_col=count_col, level=menu_level)

    await bot_send_message(chat_id=hse_user_id,
                           text=Messages.Choose.main_category, reply_markup=reply_markup)
    return True


async def get_and_send_main_locations_data(call: types.CallbackQuery, callback_data: dict = None,
                                           user_id: int | str = None) -> bool:
    """Получение данных main_locations

    :param user_id:
    :param callback_data:
    :param call:
    :return: bool
    """
    hse_user_id = call.message.chat.id if call else user_id
    previous_level = 'main_locations'
    this_level = 'main_locations'
    next_level = 'sub_locations'.upper()

    await notify_user_for_choice(call, callback_data, level=this_level)

    short_title = get_data_list(next_level,
                                category=violation_data["main_location"],
                                condition='short_title'
                                )

    logger.debug(f'{short_title = }')

    data_list = get_data_list(next_level,
                              category=violation_data["main_location"],
                              condition='data_list'
                              )
    menu_level = board_config.menu_level = 1
    menu_list = board_config.menu_list = short_title
    count_col = board_config.count_col = 2
    board_config.previous_level = previous_level

    zipped_list: list = list(zip(short_title, data_list))

    text_list = await text_process(zipped_list)

    for txt in text_list:
        await bot_send_message(chat_id=hse_user_id,
                               text=txt)

    reply_markup = await build_inlinekeyboard(
        some_list=menu_list, num_col=count_col, level=menu_level, previous_level=previous_level
    )

    await bot_send_message(chat_id=hse_user_id,
                           text=Messages.Choose.sub_location, reply_markup=reply_markup)
    return True


async def get_and_send_null_sub_locations_data(call: types.CallbackQuery, callback_data: dict = None,
                                               user_id: int | str = None) -> bool:
    """Получение данных sub_location

    :param user_id:
    :param callback_data:
    :param call:
    :return: bool
    """
    hse_user_id = call.message.chat.id if call else user_id
    previous_level: str = 'main_locations'
    this_level: str = 'sub_locations'
    next_level: str = 'main_category'.upper()

    await notify_user_for_choice(call, callback_data, level=this_level)

    menu_level = board_config.menu_level = 1
    menu_list = board_config.menu_list = get_data_list(next_level)
    count_col = board_config.count_col = 2
    board_config.previous_level = previous_level

    reply_markup = await build_inlinekeyboard(
        some_list=menu_list, num_col=count_col, level=menu_level, previous_level=previous_level
    )
    await bot_send_message(chat_id=hse_user_id,
                           text=Messages.Choose.main_category, reply_markup=reply_markup)
    return True


async def get_and_send_sub_locations_data(call: types.CallbackQuery, callback_data: dict = None,
                                          user_id: int | str = None) -> bool:
    """Получение данных sub_location

    :param user_id:
    :param callback_data:
    :param call:
    :return: bool
    """
    hse_user_id = call.message.chat.id if call else user_id
    previous_level: str = 'main_locations'
    this_level: str = 'sub_locations'
    next_level: str = 'main_category'.upper()

    await notify_user_for_choice(call, callback_data, level=this_level)

    menu_level = board_config.menu_level = 1
    menu_list = board_config.menu_list = get_data_list(next_level)
    count_col = board_config.count_col = 2
    board_config.previous_level = previous_level

    reply_markup = await build_inlinekeyboard(
        some_list=menu_list, num_col=count_col, level=menu_level, previous_level=previous_level
    )
    await bot_send_message(chat_id=hse_user_id,
                           text=Messages.Choose.main_category, reply_markup=reply_markup)
    return True


async def get_and_send_main_category_data(call: types.CallbackQuery, callback_data: dict = None,
                                          user_id: int | str = None) -> bool:
    """Получение данных sub_location

    :param user_id:
    :param callback_data:
    :param call:
    :return: bool
    """
    hse_user_id = call.message.chat.id if call else user_id
    previous_level: str = 'main_locations'
    this_level: str = 'main_category'
    next_level: str = 'category'.upper()

    await notify_user_for_choice(call, callback_data, level=this_level)

    menu_level = board_config.menu_level = 1
    menu_list = board_config.menu_list = get_data_list(next_level)
    count_col = board_config.count_col = 1
    board_config.previous_level = previous_level

    reply_markup = await build_inlinekeyboard(
        some_list=menu_list, num_col=count_col, level=menu_level, previous_level=previous_level
    )
    await bot_send_message(chat_id=hse_user_id,
                           text=Messages.Choose.category, reply_markup=reply_markup)
    return True


async def get_and_send_category_data(call: types.CallbackQuery, callback_data: dict = None,
                                     user_id: int | str = None) -> bool:
    """ Получение данных category

    :param user_id:
    :param call:
    :param callback_data:
    :return: bool
    """
    hse_user_id = call.message.chat.id if call else user_id
    previous_level: str = 'main_category'
    this_level: str = 'category'
    next_level: str = 'normative_documents'.upper()

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

    text_list = await text_process(zipped_list)

    for txt in text_list:
        await bot_send_message(chat_id=hse_user_id,
                               text=txt)

    reply_markup = await build_inlinekeyboard(
        some_list=menu_list, num_col=count_col, level=menu_level, previous_level=previous_level
    )
    await bot_send_message(chat_id=hse_user_id,
                           text=Messages.Choose.normative_documents, reply_markup=reply_markup)
    return True


async def get_and_send_null_normative_documents_data(call: types.CallbackQuery,
                                                     callback_data: dict = None,
                                                     user_id: int | str = None) -> bool:
    """ Получение данных normative_documents

    :param user_id:
    :param call:
    :param callback_data:
    :return: bool
    """
    hse_user_id = call.message.chat.id if call else user_id
    previous_level: str = 'category'
    this_level: str = 'normative_documents'
    next_level: str = 'violation_category'.upper()

    await notify_user_for_choice(call, callback_data, level=this_level)

    menu_level = board_config.menu_level = 1
    menu_list = board_config.menu_list = get_data_list(next_level)
    count_col = board_config.count_col = 2
    board_config.previous_level = previous_level

    reply_markup = await build_inlinekeyboard(
        some_list=menu_list, num_col=count_col, level=menu_level, previous_level=previous_level
    )
    await bot_send_message(chat_id=hse_user_id,
                           text=Messages.Choose.violation_category, reply_markup=reply_markup)
    return True


async def get_and_send_normative_documents_data(call: types.CallbackQuery, callback_data: dict = None,
                                                user_id: int | str = None) -> bool:
    """ Получение данных normative_documents

    :param user_id:
    :param call:
    :param callback_data:
    :return: bool
    """
    hse_user_id = call.message.chat.id if call else user_id
    previous_level: str = 'category'
    this_level: str = 'normative_documents'
    next_level: str = 'violation_category'.upper()

    await notify_user_for_choice(call, callback_data, level=this_level)

    menu_level = board_config.menu_level = 1
    menu_list = board_config.menu_list = get_data_list(next_level)
    count_col = board_config.count_col = 2
    board_config.previous_level = previous_level

    reply_markup = await build_inlinekeyboard(
        some_list=menu_list, num_col=count_col, level=menu_level, previous_level=previous_level
    )
    await bot_send_message(chat_id=hse_user_id,
                           text=Messages.Choose.category, reply_markup=reply_markup)
    return True


async def get_and_send_violation_category_data(call: types.CallbackQuery, callback_data: dict = None,
                                               user_id: int | str = None) -> bool:
    """Получение данных violation_category

    :param user_id:
    :param call:
    :param callback_data:
    :return: bool
    """
    hse_user_id = call.message.chat.id if call else user_id
    previous_level: str = 'category'
    this_level: str = 'violation_category'
    next_level: str = 'general_contractors'.upper()

    await notify_user_for_choice(call, callback_data, level=this_level)

    menu_level = board_config.menu_level = 1
    menu_list = board_config.menu_list = get_data_list(next_level)
    count_col = board_config.count_col = 1
    board_config.previous_level = previous_level

    reply_markup = await build_inlinekeyboard(
        some_list=menu_list, num_col=count_col, level=menu_level, previous_level=previous_level
    )
    await bot_send_message(chat_id=hse_user_id,
                           text=Messages.Choose.general_constractor, reply_markup=reply_markup)
    return True


async def get_and_send_general_contractors_data(call: types.CallbackQuery, callback_data: dict = None,
                                                user_id: int | str = None) -> bool:
    """Получение данных general_contractors

    :param user_id:
    :param call:
    :param callback_data:
    :return: bool
    """
    hse_user_id = call.message.chat.id if call else user_id
    previous_level: str = 'violation_category'
    this_level: str = 'general_contractors'
    next_level: str = 'incident_level'.upper()

    await notify_user_for_choice(call, callback_data, level=this_level)

    menu_level = board_config.menu_level = 1
    menu_list = board_config.menu_list = get_data_list(next_level)
    count_col = board_config.count_col = 1
    board_config.previous_level = previous_level

    reply_markup = await build_inlinekeyboard(
        some_list=menu_list, num_col=count_col, level=menu_level, previous_level=previous_level
    )
    await bot_send_message(chat_id=hse_user_id,
                           text=Messages.Choose.incident_level, reply_markup=reply_markup)
    return True


async def get_and_send_incident_level_data(call: types.CallbackQuery, callback_data: dict = None,
                                           user_id: int | str = None) -> bool:
    """Получение данных incident_level

    :param user_id:
    :param call:
    :param callback_data:
    :return: bool
    """
    hse_user_id = call.message.chat.id if call else user_id
    previous_level: str = 'general_contractors'
    this_level: str = 'incident_level'
    next_level: str = 'act_required'.upper()

    await notify_user_for_choice(call, callback_data, level=this_level)

    menu_level = board_config.menu_level = 1
    menu_list = board_config.menu_list = get_data_list(next_level)
    count_col = board_config.count_col = 1
    board_config.previous_level = previous_level

    reply_markup = await build_inlinekeyboard(
        some_list=menu_list, num_col=count_col, level=menu_level, previous_level=previous_level
    )
    await bot_send_message(chat_id=hse_user_id,
                           text=Messages.Choose.act_required, reply_markup=reply_markup)
    return True


async def get_and_send_act_required_data(call: types.CallbackQuery, callback_data: dict = None,
                                         user_id: int | str = None) -> bool:
    """Получение данных act_required

    :param user_id:
    :param call:
    :param callback_data:
    :return: bool
    """
    hse_user_id = call.message.chat.id if call else user_id
    previous_level: str = 'incident_level'
    this_level: str = 'act_required'
    next_level: str = 'elimination_time'.upper()

    await notify_user_for_choice(call, callback_data, level=this_level)

    menu_level = board_config.menu_level = 1
    menu_list = board_config.menu_list = get_data_list(next_level)
    count_col = board_config.count_col = 2
    board_config.previous_level = previous_level

    reply_markup = await build_inlinekeyboard(
        some_list=menu_list, num_col=count_col, level=menu_level, previous_level=previous_level
    )
    await bot_send_message(chat_id=hse_user_id,
                           text=Messages.Choose.elimination_time, reply_markup=reply_markup)
    return True


async def get_and_send_elimination_time_data(call: types.CallbackQuery, callback_data: dict = None,
                                             user_id: int | str = None) -> bool:
    """Получение данных act_required

    :param user_id:
    :param call:
    :param callback_data:
    :return: bool
    """
    hse_user_id = call.message.chat.id if call else user_id
    board_config.previous_level = ''

    await notify_user_for_choice(call, callback_data, level='act_required')

    await bot_send_message(chat_id=hse_user_id,
                           text=Messages.Enter.description_violation)

    # Вызов состояния ожидания текстового ответа от пользователя
    await AnswerUserState.description.set()
    return True


async def notify_user_for_choice(call: types.CallbackQuery, callback_data: dict, level: str,
                                 user_id: int | str = None) -> bool:
    """Уведомление пользователя о выборе + логирование

    :param level: str
    :param user_id: int | str
    :param call:
    :param callback_data:
    :return None :
    """
    hse_user_id = call.message.chat.id if call else user_id
    await call.message.edit_reply_markup()
    await bot_send_message(chat_id=hse_user_id, text=f"Выбрано: {call.data}")
    logger.debug(f"{hse_user_id = } Выбрано: {call.data}")

    if callback_data:
        logger.debug(f"{hse_user_id = } Выбрано: {callback_data.get('action', None)}")
        logger.debug(f"User {call.message.chat.id} choices {callback_data.get('action', None)} {level}")
    return True


async def text_process(zipped_list: list) -> list:
    """Формирование тела сообщения

    :param zipped_list:
    :return: bool
    """

    text = '\n\n'.join(str(item[0]) + " : " + str(item[1]) for item in zipped_list)

    if len(text) <= 3500:
        return [text]

    text = ''
    text_list = []
    for item in zipped_list:
        if item[0][0] == '#': continue

        text = text + f' \n\n {str(item[0])} : {str(item[1])}'
        if len(text) > 3500:
            text_list.append(text)
            text = ''

    return text_list


async def test():
    previous_level: str = 'main_category'
    this_level: str = 'category'
    next_level: str = 'normative_documents'.upper()

    short_title = get_data_list(next_level,
                                category='ТС/Спецтехника',
                                condition='short_title'
                                )
    data_list = get_data_list(next_level,
                              category='ТС/Спецтехника',
                              condition='data_list'
                              )
    menu_level = board_config.menu_level = 1
    menu_list = board_config.menu_list = short_title
    count_col = board_config.count_col = 2
    board_config.previous_level = previous_level
    board_config.this_level = this_level

    zipped_list: list = list(zip(short_title, data_list))

    text_list = await text_process(zipped_list)

    for txt in text_list:
        print(txt)
        # await bot_send_message(text=txt)

    reply_markup = await build_inlinekeyboard(
        some_list=menu_list, num_col=count_col, level=menu_level, previous_level=previous_level
    )
    print(reply_markup)


if __name__ == '__main__':
    asyncio.run(test())
