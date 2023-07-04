from loader import logger

logger.debug(f"{__name__} start import")
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup,
                           ReplyKeyboardRemove)
from apps.core.bot.data import board_config
from apps.core.bot.filters.custom_filters import is_private
from apps.core.bot.messages.messages import Messages
from apps.core.bot.states import DataUserState
from apps.core.utils.generate_report.get_file_list import (
    get_json_file_list, get_registration_json_file_list, get_report_file_list)
from apps.core.utils.json_worker.read_json_file import read_json_file
from apps.core.utils.secondary_functions.get_filepath import \
    get_file_path_user_data
from apps.MyBot import MyBot, bot_send_message

logger.debug(f"{__name__} finish import")


@MyBot.dp.callback_query_handler(is_private,
                                 lambda call: call.data in [item for item in board_config.menu_list]
    , state=DataUserState.user_data)
async def view_user_data_states_answer(call: types.CallbackQuery, state: FSMContext):
    """Отмена регистрации

    :param call:
    :param state:
    :return:
    """
    await DataUserState.user_data.set()

    chat_id: int = call.message.chat.id
    state_name = await get_state_storage_name(state=state, chat_id=chat_id)
    await view_user_data(chat_id=chat_id, view_data=call.data, state_name=state_name)

    await state.finish()


@MyBot.dp.message_handler(is_private, Text(equals=Messages.correct_cancel), state=DataUserState.all_states)
async def cancel(message: types.Message, state: FSMContext):
    """Отмена регистрации

    :param message:
    :param state:
    :return:
    """
    await state.finish()
    return await message.reply(Messages.Viewer.canceled, reply_markup=ReplyKeyboardRemove())


async def get_state_storage_name(state: FSMContext, chat_id: int):
    """Получение имени состояния state[state]

    """
    state_storage: dict = dict(state.storage.data)
    state_name: str = state_storage.get(f'{chat_id}').get(f'{chat_id}').get('state').split(':')[-1]

    return state_name


async def view_user_data(*, chat_id: int, view_data, state_name: str):
    """Обработка состояний из get_state_storage_name и данных correct_data

    :param chat_id:
    :param view_data:
    :param state_name:
    :return:
    """
    user_chat_id: str = ''
    registration_file_list: list = []
    params: dict = {}

    try:
        if isinstance(view_data, str):
            user_chat_id: str = view_data.split(' ')[0]
    except Exception as callback_err:
        logger.error(f"{chat_id= } {repr(callback_err)}")

    if user_chat_id:
        registration_file_list = await get_registration_json_file_list(chat_id=user_chat_id)

    if not registration_file_list:
        logger.warning(Messages.Error.registration_file_list_not_found)
        await bot_send_message(chat_id=chat_id, text=Messages.Error.file_list_not_found)

    registration_data = await read_json_file(registration_file_list)
    if not registration_data:
        logger.error(f"registration_data is empty")
        return

    params['all_files'] = True
    params['file_path'] = await get_file_path_user_data(chat_id=user_chat_id)

    registration_text = await get_registration_text(registration_data)

    report_file_list = await get_report_file_list(chat_id=user_chat_id, params=params)
    if report_file_list:
        report_file_text: str = f'Отчетов создано: {len(report_file_list)}'
        registration_text = f'{registration_text}\n {report_file_text}'

    json_file_list: list = await get_json_file_list(chat_id=user_chat_id, params=params)
    if json_file_list:
        json_file_list_text: str = f'Нарушений в базе: {len(json_file_list)}'
        registration_text = f'{registration_text}\n {json_file_list_text}'

    reply_markup = InlineKeyboardMarkup()
    reply_markup.add(InlineKeyboardButton(text='Url', url=f"tg://user?id={registration_data.get('user_id')}"))

    await bot_send_message(chat_id=chat_id, text=registration_text, reply_markup=reply_markup)

    await bot_send_message(chat_id=chat_id,
                           text=Messages.Successfully.registration_data_received,
                           reply_markup=ReplyKeyboardRemove())


async def get_registration_text(registration_data) -> str:
    """Получение данных о регистрации в текстовом виде

    :param registration_data:
    :return:
    """
    if registration_data:
        registration_data_text: str = \
            f"Данные регистрации: \n\n" \
            f"ФИО: {registration_data.get('name')} \n" \
            f"Должность: {registration_data.get('function')} \n" \
            f"Место работы: {registration_data.get('name_location')} \n" \
            f"Смена: {registration_data.get('work_shift')} \n" \
            f"Телефон: {registration_data.get('phone_number')} \n" \
            f"user_id {registration_data.get('user_id')} \n" \
            f"folder id https://drive.google.com/drive/folders/{registration_data.get('parent_id')} \n"

        return registration_data_text
    return ''
