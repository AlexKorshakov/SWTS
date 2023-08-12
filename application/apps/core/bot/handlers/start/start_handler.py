from __future__ import annotations

from apps.core.bot.messages.messages_test import msg
from apps.core.database.db_utils import db_update_hse_user_language
from apps.core.settyngs import get_sett
from apps.core.utils.secondary_functions.get_filepath import get_user_registration_file, create_file_path
from loader import logger

logger.debug(f"{__name__} start import")

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command, Text
from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove
from apps.core.bot.bot_utils.check_user_registration import check_user_access
from apps.core.bot.data import board_config
from apps.core.bot.data.category import get_data_list
from apps.core.bot.filters.custom_filters import is_private
from apps.core.bot.keyboards.inline.build_castom_inlinekeyboard import \
    build_inlinekeyboard
from apps.core.bot.messages.messages import Messages
from apps.core.bot.reports.report_data import user_data
from apps.core.bot.states import RegisterState
from apps.core.utils.data_recording_processor.set_user_registration_data import \
    registration_data
from apps.core.utils.misc import rate_limit
from apps.MyBot import MyBot, bot_send_message

logger.debug(f"{__name__} finish import")


@rate_limit(limit=20)
@MyBot.dp.message_handler(Command('start'), is_private)
async def start(message: types.Message, user_id: int | str = None):
    """Начало регистрации пользователя

    :param user_id: id пользователя
    :param message:
    :return:
    """

    hse_user_id = message.chat.id if message else user_id
    logger.debug(f'{hse_user_id = }')
    logger.info(f'User @{message.from_user.username} : {hse_user_id} start work')

    if not await check_user_access(chat_id=hse_user_id, message=message):
        return

    if not get_sett(cat='enable_features', param='choose_language').get_set():
        await bot_send_message(chat_id=hse_user_id, text=Messages.HSEUserAnswer.user_access_success)
        user_data["user_id"] = hse_user_id
        user_data['reg_user_file'] = await get_user_registration_file(user_id=str(hse_user_id))

        await create_file_path(path=user_data['reg_user_file'])

        hi_text: str = f'{Messages.hi} {message.chat.username}! \n\n' \
                       f'{Messages.user_greeting}\n{Messages.help_message}'

        await bot_send_message(chat_id=hse_user_id, text=hi_text)
        return

    language_list: list = await get_language_list(message, user_id=hse_user_id)
    text_violations: str = 'Выберите язык / Choose language'

    reply_markup = await build_inlinekeyboard(
        some_list=language_list, num_col=1, level=1, called_prefix='select_lang_'
    )

    await bot_send_message(chat_id=hse_user_id, text=text_violations, reply_markup=reply_markup)

    # await RegisterState.name.set()
    # reply_markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    # reply_markup.add(Messages.Registration.cancel)
    # await MyBot(hse_user_id, Messages.Ask.name, reply_markup=reply_markup)


@MyBot.dp.callback_query_handler(lambda call: 'select_lang_' in call.data)
async def call_correct_item_answer(call: types.CallbackQuery, user_id: str | int = None):
    """Обработка ответов
    """

    hse_user_id = call.message.chat.id if call else user_id
    logger.debug(f'{hse_user_id = } ::: {call.data = }')

    # await bot_delete_markup(message=call.message)

    character_language: str = call.data.split('_')[-1]
    result: bool = await db_update_hse_user_language(value=character_language, hse_id=hse_user_id)

    if result:
        text_violations: str = await msg(hse_user_id, cat='main', msge="application_language",
                                         default=Messages.application_language).g_mas()
        await bot_send_message(chat_id=hse_user_id, text=f'{text_violations}')

    user_data["user_id"] = hse_user_id
    user_data['reg_user_file'] = await get_user_registration_file(user_id=str(hse_user_id))

    await create_file_path(path=user_data['reg_user_file'])

    hi_text: str = f'{await msg(hse_user_id, cat="main", msge="hi", default=Messages.hi).g_mas()} ' \
                   f'{call.message.chat.username}! \n\n' \
                   f'{await msg(hse_user_id, cat="main", msge="user_access_success", default=Messages.HSEUserAnswer.user_access_success).g_mas()} \n\n' \
                   f'{await msg(hse_user_id, cat="main", msge="user_greeting", default=Messages.user_greeting).g_mas()} \n\n' \
                   f'{await msg(hse_user_id, cat="help", msge="help_message", default=Messages.help_message).g_mas()}'

    await bot_send_message(chat_id=hse_user_id, text=hi_text)


async def get_language_list(message: types.Message, user_id: int | str = None):
    """Выбор языка интерфейса бота

    """
    hse_user_id = message.chat.id if message else user_id

    lang_list: list = await msg(hse_user_id).get_lang_in_main()
    return lang_list


@MyBot.dp.message_handler(is_private, Text(equals=Messages.cancel), state=RegisterState.all_states)
async def cancel(message: types.Message, state: FSMContext):
    """Отмена регистрации
    :param message:
    :param state:
    :return:
    """
    await state.finish()
    return await message.reply(Messages.Registration.canceled, reply_markup=ReplyKeyboardRemove())


@MyBot.dp.message_handler(is_private, state=RegisterState.name)
async def enter_name(message: types.Message, state: FSMContext):
    """Обработка ввода имени пользователя
    :param message:
    :param state:
    :return:
    """
    user_data['name'] = message.text

    await RegisterState.next()
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(Messages.Registration.cancel)
    return await message.reply(Messages.Ask.function, reply_markup=markup)


@MyBot.dp.message_handler(is_private, state=RegisterState.function)
async def enter_function(message: types.Message, state: FSMContext):
    """Обработка ввода должности пользователя
    :param message:
    :param state:
    :return:
    """
    user_data['function'] = message.text

    await RegisterState.next()
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(Messages.Registration.cancel)
    return await message.reply(Messages.Ask.phone_number, reply_markup=markup)


@MyBot.dp.message_handler(is_private, state=RegisterState.phone_number)
async def enter_phone_number(message: types.Message, state: FSMContext):
    """Обработка ввода номера телефона пользователя
    :param message:
    :param state:
    :return:
    """
    if not message.text.startswith("+") or not message.text.strip("+").isnumeric():
        return await message.reply(Messages.Error.invalid_input)

    user_data["phone_number"] = int(message.text.strip("+"))

    menu_level = board_config.menu_level = 2
    menu_list = board_config.menu_list = get_data_list("WORK_SHIFT")

    reply_markup = await build_inlinekeyboard(some_list=menu_list, num_col=1, level=menu_level)
    await RegisterState.next()
    return await message.reply(Messages.Ask.work_shift, reply_markup=reply_markup)


@MyBot.dp.message_handler(is_private, state=RegisterState.work_shift)
async def enter_work_shift(message: types.Message, state: FSMContext):
    """Обработка рабочей смены
    """
    user_data["work_shift"] = str(message.text)

    await RegisterState.next()
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(Messages.Registration.cancel)
    return await message.reply(Messages.Ask.location, reply_markup=markup)


@MyBot.dp.callback_query_handler(is_private, lambda call: call.data in get_data_list("WORK_SHIFT"),
                                 state=RegisterState.work_shift)
async def work_shift_answer(call: types.CallbackQuery):
    """Обработка ответов содержащихся в WORK_SHIFT
    """
    chat_id = call.message.chat.id
    for i in get_data_list("WORK_SHIFT"):
        try:
            if call.data == i:
                logger.debug(f"{chat_id = } Выбрано: {i}")
                user_data["work_shift"] = i
                await bot_send_message(chat_id=chat_id, text=f"Выбрано: {i}")
                # await write_json_file(data=violation_data, name=violation_data["json_full_name"])

                await call.message.edit_reply_markup()

                METRO = [list(item.keys())[0] for item in get_data_list("METRO_STATION")]

                menu_level = board_config.menu_level = 2
                menu_list = board_config.menu_list = METRO

                reply_markup = await build_inlinekeyboard(some_list=menu_list, num_col=1, level=menu_level,
                                                          step=len(menu_list))
                await bot_send_message(chat_id=chat_id, text="Выберите строительную площадку",
                                       reply_markup=reply_markup)
                break

        except Exception as callback_err:
            logger.error(f"{repr(callback_err)}")

    await RegisterState.next()


@MyBot.dp.callback_query_handler(is_private,
                                 lambda call: call.data in [list(item.keys())[0] for item in
                                                            get_data_list("METRO_STATION")],
                                 state=RegisterState.location)
async def enter_location_answer(call: types.CallbackQuery, state: FSMContext):
    """Обработка ответов содержащихся в METRO_STATION
    """
    chat_id = call.message.chat.id

    for i in [list(item.keys())[0] for item in get_data_list("METRO_STATION")]:
        try:
            if call.data == i:
                user_data["name_location"] = i
                await bot_send_message(chat_id=chat_id, text=f"Выбрано: {i}")
                await call.message.edit_reply_markup()
                break

        except Exception as callback_err:
            logger.error(f"{repr(callback_err)}")

    await state.finish()
    await registration_data(call.message, user_data)
