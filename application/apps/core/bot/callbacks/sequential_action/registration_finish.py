import datetime

from apps.core.bot.bot_utils.check_user_registration import get_hse_user_data
from apps.core.bot.reports.report_data import ViolationData
from apps.core.bot.reports.report_data_preparation import set_violation_atr_data
from apps.core.database.db_utils import get_year_message, get_month_message, get_week_message, \
    db_get_data_dict_from_table_with_id
from apps.core.utils.secondary_functions.get_part_date import get_day_message, get_day_of_year_message, \
    get_quarter_message
from loader import logger

logger.debug(f"{__name__} start import")
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from apps.MyBot import MyBot, bot_send_message

from apps.core.utils.data_recording_processor.set_user_violation_data import pre_set_violation_data

logger.debug(f"{__name__} finish import")


@MyBot.dp.message_handler(Text(equals='завершить регистрацию', ignore_case=True), state=ViolationData.all_states)
async def registration_finish_handler(message: types.Message, state: FSMContext, user_id: str = None):
    """Обработчик сообщений содержащих 'завершить регистрацию'

    """
    hse_user_id = message.chat.id if message else user_id

    await bot_send_message(chat_id=hse_user_id,
                           text="Запущена процедура регистрации данных. Дождитесь сообщения об окончании.")

    await update_violation_data(chat_id=hse_user_id, message=message, state=state)

    await pre_set_violation_data(message, state=state)

    await state.finish()

    await bot_send_message(chat_id=hse_user_id, text="Данные зарегистрированы")


async def update_violation_data(chat_id, message, state):
    """

    :param chat_id:z
    :param message:
    :param state:
    :return:
    """

    # violation_data["user_id"] = chat_id
    await state.update_data(user_id=chat_id)
    await set_violation_atr_data("user_id", chat_id, state=state)

    # violation_data["violation_id"] = message.message_id
    # await state.update_data(violation_id=message.message_id)
    # await set_violation_atr_data("violation_id", message.message_id, state=state)

    # violation_data["user_fullname"] = message.from_user.full_name
    await state.update_data(user_fullname=message.from_user.full_name)
    await set_violation_atr_data("user_fullname", message.from_user.full_name, state=state)

    # violation_data["now"] = str(datetime.datetime.now())
    # await state.update_data(now=str(datetime.datetime.now()))
    await set_violation_atr_data("now", str(datetime.datetime.now()), state=state)

    # violation_data["status"] = 'В работе'
    await state.update_data(status='В работе')
    await set_violation_atr_data("status", 'В работе', state=state)

    user_registration_data: dict = await get_hse_user_data(message=message)

    location = await db_get_data_dict_from_table_with_id(
        table_name='core_location',
        post_id=user_registration_data.get("hse_location", None)
    )
    # violation_data["location"] = location['title']
    await state.update_data(location=location['title'])
    await set_violation_atr_data("location", location['title'], state=state)

    work_shift = await db_get_data_dict_from_table_with_id(
        table_name='core_workshift',
        post_id=user_registration_data.get("hse_work_shift", None)
    )
    # violation_data["work_shift"] = work_shift['title']
    await state.update_data(work_shift=work_shift['title'])
    await set_violation_atr_data("work_shift", work_shift['title'], state=state)

    # violation_data["hse_id"] = user_registration_data.get("id", None)
    await state.update_data(hse_id=user_registration_data.get("id", None))
    await set_violation_atr_data("hse_id", user_registration_data.get("id", None), state=state)

    # violation_data["function"] = user_registration_data.get("hse_function", None)
    await state.update_data(function=user_registration_data.get("hse_function", None))
    await set_violation_atr_data("function", user_registration_data.get("hse_function", None), state=state)

    # violation_data["name"] = user_registration_data.get("hse_full_name", None)
    await state.update_data(name=user_registration_data.get("hse_full_name", None))
    await set_violation_atr_data("name", user_registration_data.get("hse_full_name", None), state=state)

    # violation_data["parent_id"] = user_registration_data.get("parent_id")
    await state.update_data(parent_id=user_registration_data.get("parent_id"))
    await set_violation_atr_data("parent_id", user_registration_data.get("parent_id"), state=state)

    # violation_data["main_location"] = ''
    await state.update_data(main_location='')
    await set_violation_atr_data("main_location", '', state=state)

    # violation_data["main_location_id"] = ''
    await state.update_data(main_location_id='')
    await set_violation_atr_data("main_location_id", '', state=state)

    # violation_data["category"] = ''
    await state.update_data(category='')
    await set_violation_atr_data("category", '', state=state)

    # violation_data["day"] = await get_day_message()
    await state.update_data(day=await get_day_message())
    await set_violation_atr_data("day", await get_day_message(), state=state)

    # violation_data["week"] = await get_week_message()
    await state.update_data(week=await get_week_message())
    await set_violation_atr_data("week", await get_week_message(), state=state)

    # violation_data["quarter"] = await get_quarter_message()
    await state.update_data(quarter=await get_quarter_message())
    await set_violation_atr_data("quarter", await get_quarter_message(), state=state)

    # violation_data["day_of_year"] = await get_day_of_year_message()
    await state.update_data(day_of_year=await get_day_of_year_message())
    await set_violation_atr_data("day_of_year", await get_day_of_year_message(), state=state)

    # violation_data["month"] = await get_month_message()
    await state.update_data(month=await get_month_message())
    await set_violation_atr_data("month", await get_month_message(), state=state)

    # violation_data["year"] = await get_year_message()
    await state.update_data(year=await get_year_message())
    await set_violation_atr_data("year", await get_year_message(), state=state)

    deta = await get_day_message() + ":" + await get_month_message() + ":" + await get_year_message()
    # violation_data["deta"] = deta
    await state.update_data(deta=deta)
    await set_violation_atr_data("deta", deta, state=state)
