from apps.core.bot.reports.report_data import ViolationData
from loader import logger

logger.debug(f"{__name__} start import")
from aiogram import types
from apps.core.bot.callbacks.sequential_action.data_answer import (get_and_send_act_required_data,
                                                                   get_and_send_category_data,
                                                                   get_and_send_elimination_time_data,
                                                                   get_and_send_general_contractors_data,
                                                                   get_and_send_incident_level_data,
                                                                   get_and_send_main_category_data,
                                                                   get_and_send_normative_documents_data,
                                                                   get_and_send_null_normative_documents_data,
                                                                   get_and_send_null_sub_locations_data,
                                                                   get_and_send_sub_locations_data,
                                                                   get_and_send_violation_category_data,
                                                                   get_and_send_start_main_locations_data)
from apps.core.bot.callbacks.sequential_action.category import _PREFIX_ND, get_data_list, _PREFIX_POZ
from apps.core.bot.keyboards.inline.build_castom_inlinekeyboard import move_action
from apps.core.bot.reports.report_data_preparation import set_violation_atr_data
from apps.MyBot import MyBot
from aiogram.dispatcher import FSMContext

logger.debug(f"{__name__} finish import")


@MyBot.dp.callback_query_handler(move_action.filter(action=["pre_paragraph"]), state=ViolationData.all_states)
async def previous_paragraph_answer(call: types.CallbackQuery, callback_data: dict,
                                    user_id: [int, str] = None, state: FSMContext = None):
    """Обработка ответов содержащихся в previous_paragraph
    """

    chat_id = call.message.chat.id if call else user_id

    v_data: dict = await state.get_data()

    if callback_data['previous_value'] == 'main_locations':
        await get_and_send_start_main_locations_data(call, callback_data, state=state)

    elif callback_data['previous_value'] == "sub_location":

        if call.data == _PREFIX_POZ + "0":
            await get_and_send_null_sub_locations_data(call, callback_data, state=state)

        print(f"{call.data}")
        condition: dict = {
            "data": call.data,
            "category_in_db": "SUB_LOCATIONS",
        }
        sub_loc = get_data_list("SUB_LOCATIONS",
                                category=v_data["main_location"],
                                condition=condition)
        if not sub_loc:
            await set_violation_atr_data("sub_location", call.data, state=state)

        await set_violation_atr_data("sub_location", sub_loc[0].get('title', None), state=state)

        await get_and_send_sub_locations_data(call, callback_data, state=state)

    elif callback_data['previous_value'] == "main_category":
        await get_and_send_main_category_data(call, callback_data, state=state)

    elif callback_data['previous_value'] == "category":
        await get_and_send_category_data(call, callback_data, state=state)

    elif callback_data['previous_value'] == "normative_documents":

        if call.data == _PREFIX_ND + "0":
            await get_and_send_null_normative_documents_data(call, state=state)

        condition: dict = {
            "data": call.data,
            "category_in_db": "NORMATIVE_DOCUMENTS",
        }
        nd_data: list = get_data_list("NORMATIVE_DOCUMENTS",
                                      category=v_data["category"],
                                      condition=condition)
        if not nd_data:
            await set_violation_atr_data("normative_documents", call.data, state=state)

        await set_violation_atr_data("normative_documents", nd_data[0].get('title', None), state=state)
        await set_violation_atr_data("normative_documents_normative", nd_data[0].get('normative', None), state=state)
        await set_violation_atr_data("normative_documents_procedure", nd_data[0].get('procedure', None), state=state)

        await get_and_send_normative_documents_data(call, state=state)

    elif callback_data['previous_value'] == "violation_category":
        await get_and_send_violation_category_data(call, callback_data, state=state)

    elif callback_data['previous_value'] == "general_contractors":
        await get_and_send_general_contractors_data(call, callback_data, state=state)

    elif callback_data['previous_value'] == "incident_level":
        await get_and_send_incident_level_data(call, callback_data, state=state)

    elif callback_data['previous_value'] == "act_required":
        await get_and_send_act_required_data(call, callback_data, state=state)

    elif callback_data['previous_value'] == "elimination_time":
        await get_and_send_elimination_time_data(call, callback_data, state=state)

    else:
        logger.debug(f"{chat_id = }  Выбрано: {callback_data['action']}")
        logger.info(f"User {call.message.chat.id} choices {callback_data['action']}")
        logger.info(f"{call.data = }")
        logger.info(f"{callback_data = }")
