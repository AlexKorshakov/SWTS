from pprint import pprint

from aiogram import types

from app import MyBot
from apps.core.bot.callbacks.sequential_action.data_answer import \
    get_and_send_main_locations_data, \
    get_and_send_sub_locations_data, \
    get_and_send_main_category_data, \
    get_and_send_category_data, \
    get_and_send_null_normative_documents_data, \
    get_and_send_normative_documents_data, \
    get_and_send_violation_category_data, \
    get_and_send_incident_level_data, \
    get_and_send_act_required_data, \
    get_and_send_elimination_time_data, get_and_send_null_sub_locations_data, get_and_send_general_contractors_data
from apps.core.bot.data.category import get_data_list, _PREFIX_ND
from apps.core.bot.data.report_data import violation_data
from apps.core.bot.keyboards.inline.build_castom_inlinekeyboard import move_action
from apps.core.utils.json_worker.writer_json_file import write_json_file
from loader import logger

logger.debug("previous_paragraph")


@MyBot.dp.callback_query_handler(move_action.filter(action=["previous_paragraph"]))
async def previous_paragraph_answer(call: types.CallbackQuery, callback_data: dict):
    """Обработка ответов содержащихся в previous_paragraph
    """

    pprint(f'{callback_data = }')
    pprint(f'{call.data = }')
    pprint(f'{violation_data = }')
    pprint(f'{violation_data = }')
    pprint(f'{violation_data = }')
    pprint(f'{violation_data = }')

    if callback_data['previous_value'] == 'main_locations':
        await get_and_send_main_locations_data(call, callback_data)

    elif callback_data['previous_value'] == "sub_location":

        if call.data == _PREFIX_ND + "0":
            await get_and_send_null_sub_locations_data(call, callback_data)

        print(f"{call.data}")
        condition: dict = {
            "data": call.data,
            "category_in_db": "SUB_LOCATIONS",
        }
        sub_loc = get_data_list("SUB_LOCATIONS",
                                category=violation_data["main_location"],
                                condition=condition)
        if not sub_loc:
            violation_data["sub_location"] = call.data

        violation_data["sub_location"] = sub_loc[0].get('title', None)

        await write_json_file(data=violation_data, name=violation_data["json_full_name"])

        await get_and_send_sub_locations_data(call, callback_data)

    elif callback_data['previous_value'] == "main_category":
        await get_and_send_main_category_data(call, callback_data)

    elif callback_data['previous_value'] == "category":
        await get_and_send_category_data(call, callback_data)

    elif callback_data['previous_value'] == "normative_documents":

        if call.data == _PREFIX_ND + "0":
            await get_and_send_null_normative_documents_data(call)

        condition: dict = {
            "data": call.data,
            "category_in_db": "NORMATIVE_DOCUMENTS",
        }
        nd_data: list = get_data_list("NORMATIVE_DOCUMENTS",
                                      category=violation_data["category"],
                                      condition=condition)
        if not nd_data:
            violation_data["normative_documents"] = call.data

        violation_data["normative_documents"] = nd_data[0].get('title', None)
        violation_data["normative_documents_normative"] = nd_data[0].get('normative', None)
        violation_data["normative_documents_procedure"] = nd_data[0].get('procedure', None)

        await write_json_file(data=violation_data, name=violation_data["json_full_name"])

        await get_and_send_normative_documents_data(call)

    elif callback_data['previous_value'] == "violation_category":
        await get_and_send_violation_category_data(call, callback_data)

    elif callback_data['previous_value'] == "general_contractors":
        await get_and_send_general_contractors_data(call, callback_data)

    elif callback_data['previous_value'] == "incident_level":
        await get_and_send_incident_level_data(call, callback_data)

    elif callback_data['previous_value'] == "act_required":
        await get_and_send_act_required_data(call, callback_data)

    elif callback_data['previous_value'] == "elimination_time":
        await get_and_send_elimination_time_data(call, callback_data)

    else:
        logger.debug(f"Выбрано: {callback_data['action']}")
        logger.info(f"User {call.message.chat.id} choices {callback_data['action']}")
        logger.info(f"{call.data = }")
        logger.info(f"{callback_data = }")
