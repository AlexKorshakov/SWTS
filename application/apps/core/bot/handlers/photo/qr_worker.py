from __future__ import annotations
import os
import cv2
from pandas import DataFrame
from pypika import Database
from pyzbar import pyzbar
from itertools import chain

from apps.core.bot.handlers.correct_entries.correct_support import check_dataframe
from apps.core.bot.messages.messages import Messages
from apps.core.database.db_utils import db_get_table_headers, db_get_data_list, db_get_data_dict_from_table_with_id
from apps.core.database.query_constructor import QueryConstructor
from loader import logger


async def generate_text(qr_data: str | list = None) -> str:
    """Получение информации из data

    :param qr_data:
    :return:
    """
    if qr_data is None:
        return ""

    qr_data_list: list = []
    if isinstance(qr_data, list):
        qr_data_list: list = list(chain(*qr_data))

    qr_data_text: list = []
    for qr_data in qr_data_list:

        act_text: str = ''
        if isinstance(qr_data, str):
            qr_data_list: list = qr_data.split("_")
            if qr_data_list[0] != 'qr':
                return ''

            act_number = qr_data_list[-1]
            user_id = qr_data_list[-2]

            violations_df = await get_violations_df(act_number)
            act_text: str = await text_processor_act(act_number, violations_df)
            items_text: str = await text_processor_items(violations_df, hse_user_id=user_id)

            qr_data_text.append(f'{act_text}\n\n{items_text}')

    return '\n\n '.join(qr_data_text)


async def get_violations_df(act_number: str | int) -> DataFrame:
    """

    :return:
    """

    query_kwargs: dict = {
        "action": 'SELECT',
        "subject": '*',
        "conditions": {
            "act_number": act_number,
        },
    }
    query: str = await QueryConstructor(None, 'core_violations', **query_kwargs).prepare_data()

    violations_dataframe: DataFrame = await create_lite_dataframe_from_query(
        query=query, table_name='core_violations'
    )

    if violations_dataframe is None:
        logger.error(f'{Messages.Error.dataframe_is_empty}  \n{query = }')
        return ''

    if violations_dataframe.empty:
        logger.error(f'{Messages.Error.dataframe_is_empty}  \n{query = }')
        return ''

    return violations_dataframe


async def text_processor_act(act_number: int | str, act_violations_df: DataFrame) -> str:
    """Формирование текста для отправки пользователю"""

    if not act_number:
        return ''

    query_kwargs: dict = {
        "action": 'SELECT', "subject": '*',
        "conditions": {
            "act_number": act_number,
        },
    }
    query: str = await QueryConstructor(None, 'core_actsprescriptions', **query_kwargs).prepare_data()

    act_dataframe: DataFrame = await create_lite_dataframe_from_query(
        query=query, table_name='core_actsprescriptions')

    if act_dataframe.empty:
        logger.error(f'{Messages.Error.dataframe_is_empty}  \n{query = }')

    len_act_violations: int = act_dataframe.act_row_count.unique().tolist()[0]
    act_date = act_dataframe.act_date.unique().tolist()[0]

    general_constractor_id = act_dataframe.act_general_contractor_id.unique().tolist()[0]

    # act_violations_df = user_violations.copy(deep=True)
    # current_act_violations: DataFrame = act_violations_df.loc[act_violations_df['act_number'] == act_number]

    unclosed_points_df = act_violations_df.loc[act_violations_df['status_id'] != 1]
    unclosed_points: int = len(unclosed_points_df)

    general_constractor: str = await get_item_title_for_id(
        table_name='core_generalcontractor', item_id=general_constractor_id
    )

    act_description: list = []
    item_info = f'Ном: {act_number} от {act_date} {general_constractor} всего пунктов: {len_act_violations} Незакрыто: {unclosed_points}'
    act_description.append(item_info)

    header_text: str = 'Акт - предписание '
    acts_text: str = '\n'.join(act_description)

    final_text: str = f'{header_text} \n\n{acts_text}'
    return final_text


async def text_processor_items(user_violations_df: DataFrame, hse_user_id: str | int) -> str:
    """Формирование текста для отправки пользователю

    """
    unique_items_ids: list = user_violations_df.id.unique().tolist()

    items_description: list = []

    for item_id in unique_items_ids:

        item_violations_dataframe = user_violations_df.copy(deep=True)
        item_df = item_violations_dataframe.loc[item_violations_dataframe['id'] == item_id]

        if not await check_dataframe(item_violations_dataframe, hse_user_id):
            continue

        created_at = item_df['created_at'].values[0]
        item_status = await get_item_title_for_id(
            'core_status', item_id=item_df['status_id'].values[0]
        )
        item_main_category = await get_item_title_for_id(
            table_name='core_maincategory', item_id=item_df['main_category_id'].values[0]
        )
        item_category = await get_item_title_for_id(
            table_name='core_category', item_id=item_df['category_id'].values[0]
        )
        item_general_contractor_id = await get_item_title_for_id(
            table_name='core_generalcontractor', item_id=item_df['general_contractor_id'].values[0]
        )
        item_main_location = await get_item_title_for_id(
            table_name='core_mainlocation', item_id=item_df['main_location_id'].values[0]
        )
        item_sub_location = await get_item_title_for_id(
            table_name='core_sublocation', item_id=item_df['sub_location_id'].values[0]
        )
        item_description = item_df['description'].values[0]
        elimination_time = await get_item_title_for_id(
            table_name='core_eliminationtime', item_id=item_df['elimination_time_id'].values[0]
        )
        normative_documents_title = await get_item_title_for_id(
            table_name='core_normativedocuments', item_id=item_df['normative_documents_id'].values[0],
        )

        normative_documents_desc = await get_item_title_for_id(
            table_name='core_normativedocuments', item_id=item_df['normative_documents_id'].values[0],
            item_name='normative'
        )

        item_info = f'Ном пункта: {item_id} от {created_at} Статус: {item_status} \n\n' \
                    f'Устранить до: {elimination_time} \n' \
                    f'Подрядчик: {item_general_contractor_id} \n' \
                    f'Территория: {item_main_location} - {item_sub_location} \n' \
                    f'Направление: {item_main_category} \n' \
                    f'Категория: {item_category} \n' \
                    f'Описание: {item_description} \n' \
                    f'Подкатегория: {normative_documents_title} \n' \
                    f'Нормативка: {normative_documents_desc}\n'

        items_description.append(item_info)

    items_text: str = '\n'.join(items_description)

    # header_text: str = 'Выбранный пункт:'
    # footer_text: str = 'Выберите характеристику для изменения'
    #
    # final_text: str = f'{header_text} \n\n{items_text}  \n\n{footer_text}'
    return items_text


async def create_lite_dataframe_from_query(query: str, table_name: str) -> DataFrame or None:
    """Возвращает list с нарушениями

    :return: DataFrame or None
    """

    if not query:
        # logger.error(f"{LogMessage.Check.no_query} ::: {await get_now()}")
        return None

    violations_data: list = await db_get_data_list(query=query)

    if not violations_data:
        # logger.debug(f"{LogMessage.Check.no_violations} ::: {await get_now()}")
        return None

    headers = await db_get_table_headers(table_name=table_name)
    clean_headers: list = [item[1] for item in headers]

    try:
        dataframe = DataFrame(violations_data, columns=clean_headers)
        return dataframe
    except Exception as err:
        # logger.error(f"create_dataframe {repr(err)}")
        return None


async def get_item_title_for_id(table_name: str, item_id: int, item_name: str = None) -> str:
    """

    :param item_name:
    :param table_name:
    :param item_id:
    :return:
    """
    item_dict: dict = await db_get_data_dict_from_table_with_id(
        table_name=table_name,
        post_id=item_id
    )

    item_name = item_name if item_name else 'title'
    item_text: str = item_dict.get(item_name, '')
    return item_text


def read_qr_code_image(filename: str):
    """Чтение изображения

    :return:
    """
    return cv2.imread(filename)


def qr_code_reader(image) -> list:
    """Распознавание QR-кода на изображении

    :param image: - объект изображения
    :return:
    """
    # initialize the cv2 QRCode detector

    all_data: list = []
    qrcodes = pyzbar.decode(image)

    for qrcode in qrcodes:
        qrcode_data: str = qrcode.data.decode('utf-8')
        if qrcode.type == 'QRCODE':
            all_data.append(qrcode_data.split('&'))

    return all_data

    #     img = cv2.rectangle(img, (d.rect.left, d.rect.top),
    #                         (d.rect.left + d.rect.width, d.rect.top + d.rect.height), (255, 0, 0), 2)
    #     img = cv2.polylines(img, [np.array(d.polygon)], True, (0, 255, 0), 2)
    #     img = cv2.putText(img, d.data.decode(), (d.rect.left, d.rect.top + d.rect.height),
    #                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 1, cv2.LINE_AA)
    #
    # cv2.imwrite('data/dst/barcode_qrcode_opencv.jpg', img)
    #
    # detector = cv2.QRCodeDetector()
    #
    # # detect and decode
    #
    # data, bbox, straight_qrcode = detector.detectAndDecode(image)
    #
    # # if there is a QR code
    # if bbox is not None:
    #     # print(f"QRCode data: {data}")
    #     # display the image with lines
    #     # length of bounding box
    #     # n_lines = len(bbox)
    #     # for i in range(n_lines):
    #     #     # draw all lines
    #     #     point1 = tuple(bbox[i][0])
    #     #     point2 = tuple(bbox[(i + 1) % n_lines][0])
    #     #     cv2.line(img, point1, point2, color=(255, 0, 0), thickness=2)
    #
    #     return data


def display_data(img):
    """display the result

    """
    cv2.imshow("img", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def files(path):
    for file in os.listdir(path):
        if os.path.isfile(os.path.join(path, file)):
            yield file


if __name__ == '__main__':

    file_path = 'C:\\Users\\DeusEx\\Desktop\\WhatsApp\\'

    for file in files(file_path):
        img = read_qr_code_image(file_path + file)
        data = qr_code_reader(img)
        print("file: ", file, "data ", data)
