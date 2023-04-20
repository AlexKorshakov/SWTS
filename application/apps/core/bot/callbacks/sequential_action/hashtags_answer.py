import traceback

from apps.core.database.query_constructor import QueryConstructor
from loader import logger

logger.debug(f"{__name__} start import")
from apps.core.bot.data import board_config
from apps.core.bot.keyboards.inline.build_castom_inlinekeyboard import build_inlinekeyboard
from apps.core.bot.messages.messages import Messages
from apps.core.database.db_utils import db_get_data_list_no_async
from aiogram import types
from apps.core.bot.data.category import _PREFIX_ND, get_data_with_hashtags, _PREFIX_POZ
from apps.core.bot.reports.report_data import violation_data
from apps.MyBot import MyBot

logger.debug(f"{__name__} finish import")


@MyBot.dp.callback_query_handler(lambda call: call.data[0] == '#')
async def normative_documents_answer_with_hashtags(call: types.CallbackQuery) -> None:
    """Обработка ответов содержащихся в NORMATIVE_DOCUMENTS
    """

    hashtag = call.data
    logger.info(f'{call.data = }')

    # normativedocuments_hashtags:list = get_data_with_hashtags(
    #     "core_normativedocuments", item_id=violation_data.get('category_id', None))
    #
    # if call.data in normativedocuments_hashtags:
    #     previous_level = 'category'
    #
    #     menu_level = board_config.menu_level = 1
    #     menu_list = board_config.menu_list = [_PREFIX_ND + str(item[0]) for item in normativedocuments_hashtags]
    #     count_col = board_config.count_col = 2
    #     board_config.previous_level = previous_level
    #
    #     short_title: list = [_PREFIX_ND + str(item[0]) for item in normativedocuments_hashtags]
    #     data_list: list = [item[2] for item in normativedocuments_hashtags]
    #     zipped_list: list = list(zip(short_title, data_list))
    #
    #     text_list: list = text_process(zipped_list)
    #     for item_txt in text_list:
    #         await call.message.answer(text=item_txt)
    #
    #     reply_markup = await build_inlinekeyboard(
    #         some_list=menu_list, num_col=count_col, level=menu_level, previous_level=previous_level
    #     )
    #     await call.message.answer(text=Messages.Choose.normative_documents, reply_markup=reply_markup)
    #     return
    #
    # sublocation_hashtags:list = get_data_with_hashtags(
    #     "core_sublocation", item_id=violation_data.get('main_location_id', None))

    if call.data in get_data_with_hashtags("core_normativedocuments", item_id=violation_data.get('category_id', None)):
        logger.info(f'{__name__} {say_fanc_name()} NORMATIVE_DOCUMENTS')

        db_table_name = 'core_normativedocuments'
        category_id = violation_data.get('category_id', None)

        # TODO заменить на вызов конструктора QueryConstructor
        query: str = f"SELECT * FROM {db_table_name} WHERE `category_id` == {category_id} AND `hashtags` LIKE '%{hashtag}%'"

        kwargs: dict = {
            "action": 'SELECT', "subject": '*',
            "conditions": {
                "category_id": category_id,
                "hashtag": call.data,
                "hashtag_condition": 'like',
            }
        }
        query: str = await QueryConstructor(table_name=db_table_name, **kwargs).prepare_data()
        logger.info(f'{__name__} {say_fanc_name()} {query}')
        datas_query: list = db_get_data_list_no_async(query=query)

        previous_level = 'category'

        menu_level = board_config.menu_level = 1
        menu_list = board_config.menu_list = [_PREFIX_ND + str(item[0]) for item in datas_query]
        count_col = board_config.count_col = 2
        board_config.previous_level = previous_level

        short_title: list = [_PREFIX_ND + str(item[0]) for item in datas_query]
        data_list: list = [item[2] for item in datas_query]
        zipped_list: list = list(zip(short_title, data_list))

        text_list: list = text_process(zipped_list)
        for item_txt in text_list:
            await call.message.answer(text=item_txt)

        reply_markup = await build_inlinekeyboard(
            some_list=menu_list, num_col=count_col, level=menu_level, previous_level=previous_level
        )
        await call.message.answer(text=Messages.Choose.normative_documents, reply_markup=reply_markup)
        return

    if call.data in get_data_with_hashtags("core_sublocation", item_id=violation_data.get('main_location_id', None)):
        logger.info(f'{__name__} {say_fanc_name()} SUB_LOCATIONS')

        db_table_name = 'core_sublocation'
        main_location_id = violation_data.get('main_location_id', None)

        kwargs: dict = {
            "action": 'SELECT', "subject": '*',
            "conditions": {
                "main_location_id": main_location_id,
                "hashtag": call.data,
                "hashtag_condition": 'like',
            }
        }
        query: str = await QueryConstructor(table_name=db_table_name, **kwargs).prepare_data()

        logger.info(f'{__name__} {say_fanc_name()} {query}')
        datas_query: list = db_get_data_list_no_async(query=query)

        previous_level = 'main_location'

        menu_level = board_config.menu_level = 1
        menu_list = board_config.menu_list = [_PREFIX_POZ + str(item[0]) for item in datas_query]
        count_col = board_config.count_col = 2
        board_config.previous_level = previous_level

        short_title: list = [_PREFIX_POZ + str(item[0]) for item in datas_query]
        data_list: list = [item[2] for item in datas_query]

        zipped_list: list = list(zip(short_title, data_list))
        text_list: list = text_process(zipped_list)
        for item_txt in text_list:
            await call.message.answer(text=item_txt)

        reply_markup = await build_inlinekeyboard(
            some_list=menu_list, num_col=count_col, level=menu_level, previous_level=previous_level
        )
        await call.message.answer(text=Messages.Choose.normative_documents, reply_markup=reply_markup)
        return

    return None


def text_process(data_list_to_text: list) -> list:
    """Принимает data_list_to_text[] для формирования текста ответа
    Если len(text) <= 3500 - отправляет [сообщение]
    Если len(text) > 3500 - формирует list_with_parts_text = []

    :param data_list_to_text: лист с данными для формирования текста сообщения
    :return: list - list_with_parts_text
    """

    text = '\n\n'.join(str(item[0]) + " : " + str(item[1]) for item in data_list_to_text)

    if len(text) <= 3500:
        return [text]

    text = ''
    list_with_parts_text = []
    for item in data_list_to_text:

        text = text + f' \n\n {str(item[0])} : {str(item[1])}'
        if len(text) > 3500:
            list_with_parts_text.append(text)
            text = ''

    return list_with_parts_text


def say_fanc_name():
    stack = traceback.extract_stack()
    return str(stack[-2][2])


if __name__ == '__main__':
    db_table_name = 'core_normativedocuments'

    hashtag_test = '#Огнетушители'
    query_test: str = f"SELECT * FROM {db_table_name} WHERE `category_id` == {16} AND `hashtags` LIKE '%{hashtag_test}%'"
    print(f'{__name__} {say_fanc_name()} {query_test}')

    datas_query_test: list = db_get_data_list_no_async(query=query_test)
    clean_datas_query_test: list = [item[1] for item in datas_query_test]

    short_title = [_PREFIX_ND + str(item[0]) for item in datas_query_test]
    data_list = [item[2] for item in datas_query_test]
    zipped_list: list = list(zip(short_title, data_list))

    text_list = text_process(zipped_list)

    for txt in text_list:
        print(txt)
