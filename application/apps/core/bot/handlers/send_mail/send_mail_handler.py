from __future__ import print_function

import mimetypes
import os
import smtplib
import ssl
from datetime import datetime, timedelta
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from aiogram import types
from aiogram.dispatcher.filters import Command

from app import MyBot
from loader import logger

from apps.core.bot.data.category import get_data_list
from config.config import SENDER_ACCOUNT_GMAIL, SENDER_ACCOUNT_PASSWORD, SENDER

from apps.core.bot.messages.messages import Messages
from apps.core.bot.utils.generate_report.get_file_list import get_registration_json_file_list, get_report_file_list
from apps.core.bot.utils.json_worker.read_json_file import read_json_file
from apps.core.bot.utils.misc import rate_limit


from apps.core.bot.utils.secondary_functions.check_user_registration import check_user_access


@rate_limit(limit=360)
@MyBot.dp.message_handler(Command('send_mail'))
async def send_mail(message: types.Message, file_list: list = None, registration_data: dict = None):
    """Отправка сообщения с отчетом
    :param file_list:
    :param message:
    :param registration_data:
    :return:
    """

    chat_id = message.chat.id
    if not await check_user_access(chat_id=chat_id):
        return

    registration_file_list = []

    if not file_list:
        file_list = await get_report_file_list(chat_id=message.from_user.id, endswith='.pdf')
        if not file_list:
            logger.warning(Messages.Error.file_list_not_found)
            await MyBot.bot.send_message(message.from_user.id, Messages.Error.file_list_not_found)

    if not registration_data:
        registration_file_list = await get_registration_json_file_list(chat_id=message.chat.id)
        if not registration_file_list:
            logger.warning(Messages.Error.registration_file_list_not_found)
            await MyBot.bot.send_message(message.from_user.id, Messages.Error.file_list_not_found)

    registration_data = await read_json_file(registration_file_list)

    if not registration_data:
        logger.error(f"registration_data is empty")
        return

    await MyBot.bot.send_message(message.from_user.id, Messages.Successfully.registration_data_received)
    logger.info(Messages.Successfully.registration_data_received)

    location = registration_data.get("name_location", None)
    if not location:
        logger.warning(Messages.Error.location_name_not_found)
        await MyBot.bot.send_message(message.from_user.id, Messages.Error.location_name_not_found)
        return

    sent_to = []
    sent_to_cc = []
    if location in [list(item.keys())[0] for item in get_data_list("METRO_STATION")]:

        for item in get_data_list("METRO_STATION"):
            if list(item.keys())[0] == location:

                for item_to in item.get(location):
                    if list(item_to.keys())[0] == 'RS':
                        rs_list = item_to.get('RS')
                        if isinstance(rs_list, list):
                            for i in rs_list:
                                sent_to.append(i)
                        else:
                            sent_to.append(rs_list)

                    if list(item_to.keys())[0] == 'HSE':
                        hse_list = item_to.get('HSE')
                        for i in hse_list:
                            sent_to_cc.append(i)

                    if list(item_to.keys())[0] == 'SUB_HSE':
                        sub_hse_list = item_to.get('SUB_HSE')
                        for i in sub_hse_list:
                            sent_to.append(i)
                break

    if not sent_to:
        logger.error(f"SENT_TO is empty")
        await MyBot.bot.send_message(message.from_user.id, Messages.Error.list_too_send_not_found)
        return

    sent_to_cc = sent_to_cc + get_data_list("SENT_TO_СС")
    if not sent_to_cc:
        logger.error(f"SENT_TO_CC is empty")
        return

    text_send_to = ' \n'.join(sent_to)
    text_send_to_cc = ' \n'.join(sent_to_cc)
    text: str = f'{Messages.defined_recipient_list}: \n' \
                f"Получатели: \n{text_send_to} \n" \
                f"В копии: \n{text_send_to_cc} \n"

    await MyBot.bot.send_message(message.from_user.id, text=text)

    await MyBot.bot.send_message(message.from_user.id, Messages.Successfully.list_tutors_received)
    logger.info(Messages.Successfully.list_tutors_received)

    email_message = MIMEMultipart('mixed')
    email_message['From'] = f"{SENDER} <{SENDER_ACCOUNT_GMAIL}>"
    email_message['To'] = ', '.join(sent_to)
    email_message['Cc'] = ', '.join(sent_to_cc)

    isreportfile = []
    for report_file in file_list or []:
        if not os.path.isfile(report_file):
            logger.error(f"report_file {report_file} {Messages.Error.file_not_found}")
            isreportfile.append(False)
            continue

        mime_type, _ = mimetypes.guess_type(report_file)
        mime_type, mime_subtype = mime_type.split('/')

        try:
            with open(report_file, "rb") as attachment:
                p = MIMEApplication(attachment.read(), _subtype=mime_subtype)
                name = report_file.split("\\")[-1]

                p.add_header('Content-Disposition', 'attachment', filename=name)
                email_message.attach(p)
                isreportfile.append(True)
                break
        except Exception as err:
            print(str(err))
            return

    if any([file for file in isreportfile]):

        await MyBot.bot.send_message(message.from_user.id, Messages.Successfully.letter_formed)
        logger.info(Messages.Successfully.letter_formed)

        custom_date = datetime.now().strftime("%d.%m.%Y")
        date_now = str(datetime.now().strftime("%d.%m.%Y"))
        date_then = datetime.now() - timedelta(days=1)
        date_then = str(date_then.strftime("%d.%m.%Y"))

        location = registration_data["name_location"] if registration_data.get('name_location') else ''
        work_shift = registration_data["work_shift"] if registration_data.get('work_shift') else ''
        function = registration_data["function"] if registration_data.get('function') else ''
        name = registration_data["name"] if registration_data.get('name') else ''

        if registration_data.get('work_shift'):
            if work_shift.lower() == "дневная смена":
                work_shift = 'дневной смены'
                custom_date = f"{date_now}"
            else:
                work_shift = 'ночной смены'
                custom_date = f"{date_then} - {date_now}"
        else:
            work_shift = ''

        email_message['Subject'] = f'Отчет за {custom_date} по площадке {location}'
        msg_content = f'<h4>Добрый день!<br> Направляю Вам Отчет {work_shift} за {custom_date} ' \
                      f'по площадке {location}.<br>' \
                      f'Отчет составил {function} {name}.</h4>' \
                      f'<br>' \
                      f'<br>' \
                      f'</center>'
        # f'по вопросам работы бота обращайтесь {DEVELOPER_EMAIL}' \
        body = MIMEText(msg_content, 'html')
        email_message.attach(body)

        msg_full = email_message.as_string()

        context = ssl.create_default_context()

        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.ehlo()
            server.starttls(context=context)
            server.ehlo()
            server.login(SENDER_ACCOUNT_GMAIL, password=SENDER_ACCOUNT_PASSWORD)
            server.sendmail(SENDER_ACCOUNT_GMAIL,
                            to_addrs=sent_to + get_data_list("SENT_TO_СС"),
                            msg=msg_full)
            await MyBot.bot.send_message(message.from_user.id, Messages.Successfully.mail_send)
            logger.info(Messages.Successfully.mail_send)
            server.quit()

        # await asyncio.sleep(10)

    else:
        logger.error(Messages.Error.no_file_too_send)
        await MyBot.bot.send_message(message.from_user.id, Messages.Error.no_file_too_send)


