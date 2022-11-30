from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command, Text
from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove

from app import MyBot
from apps.core.utils.secondary_functions.get_filepath import get_user_registration_file, create_file_path
from loader import logger

from apps.core.bot.messages.messages import Messages
from apps.core.bot.data import board_config
from apps.core.bot.reports.report_data import user_data
from apps.core.bot.data.category import get_data_list
from apps.core.bot.states import RegisterState
from apps.core.bot.filters.custom_filters import is_private
from apps.core.utils.misc import rate_limit

from apps.core.utils.data_recording_processor.set_user_registration_data import registration_data

from apps.core.bot.keyboards.inline.build_castom_inlinekeyboard import build_inlinekeyboard


@rate_limit(limit=20)
@MyBot.dp.message_handler(Command('start'), is_private)
async def start(message: types.Message):
    """Начало регистрации пользователя
    :param message:
    :return:
    """
    user_id = str(message.from_user.id)
    user_data["user_id"] = user_id
    user_data['reg_user_file'] = await get_user_registration_file(user_id=user_id)

    await create_file_path(path=user_data['reg_user_file'])

    logger.info(f'User @{message.from_user.username}:{message.from_user.id} start work')
    await message.answer(f'{Messages.hi}, {message.from_user.full_name}!')
    await message.answer(f'{Messages.user_greeting} \n'
                         f'{Messages.help_message}')

    await RegisterState.name.set()
    reply_markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    reply_markup.add(Messages.Registration.cancel)
    await MyBot.bot.send_message(message.from_user.id, Messages.Ask.name, reply_markup=reply_markup)


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
    for i in get_data_list("WORK_SHIFT"):
        try:
            if call.data == i:
                logger.debug(f"Выбрано: {i}")
                user_data["work_shift"] = i
                await call.message.answer(text=f"Выбрано: {i}")
                # await write_json_file(data=violation_data, name=violation_data["json_full_name"])

                await call.message.edit_reply_markup()

                METRO = [list(item.keys())[0] for item in get_data_list("METRO_STATION")]

                menu_level = board_config.menu_level = 2
                menu_list = board_config.menu_list = METRO

                reply_markup = await build_inlinekeyboard(some_list=menu_list, num_col=1, level=menu_level,
                                                          step=len(menu_list))
                await call.message.answer(text="Выберите строительную площадку", reply_markup=reply_markup)
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
    for i in [list(item.keys())[0] for item in get_data_list("METRO_STATION")]:
        try:
            if call.data == i:
                user_data["name_location"] = i
                await call.message.answer(text=f"Выбрано: {i}")
                await call.message.edit_reply_markup()
                break

        except Exception as callback_err:
            logger.error(f"{repr(callback_err)}")

    await state.finish()
    await registration_data(call.message, user_data)
