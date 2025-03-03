import datetime
import os
import logging.config

from imap_tools import AND, MailBox

from config import name_and_mail, year
from dotenv import load_dotenv

from helps.utils import create_list_summ, create_output, format_output_translate

load_dotenv()

IMAP: str = os.environ['SERVER_IMAP']
MAIL_USERNAME: str = os.environ['USERNAME_MAIL']
MAIL_PASSWORD: str = os.environ['PASS_MAIL']

list_data = []

debug_logger = logging.getLogger('log_debug')

class MoneyForMonth:
    __slots__ = ('data','message_list')

    def __init__(self, data: list):
        self.data = data
        self.message_list =[]

    def request_summ(self) -> str:
        list_message = self.request_email()
        if list_message:
            messages = create_list_summ(list_message)
            output = create_output(messages)
            return format_output_translate(output)
        else:
            return "За указанный период расчетов не было"

    def request_email(self) -> list:
        start_finish_days:tuple=self.day_start_finish()
        with MailBox(IMAP).login(MAIL_USERNAME, MAIL_PASSWORD) as mailbox:
            mailbox.folder.set('Отправленные')
            criteria = AND(sent_date_gte=start_finish_days[0].date(),
                           sent_date_lt=start_finish_days[1].date(),
                           text="гривен")
            for msg in mailbox.fetch(criteria, charset = 'utf-8'):
                self.message_list.append([msg.uid, str(msg.date), msg.to, msg.text])
        return self.message_list


    def day_start_finish(self)->tuple:
        month: int = int(self.data[0])
        day_start: int = int(self.data[1])
        date_start:datetime = datetime.datetime(year, month, day_start)
        date_finish:datetime = datetime.datetime(year, month + 1, 1)
        return date_start,date_finish

class MoneyForPeriod(MoneyForMonth):

    def request_email(self) -> list:
        mails = name_and_mail.get(self.data[2])
        start_finish_days:tuple=self.day_start_finish()
        with MailBox(IMAP).login(MAIL_USERNAME, MAIL_PASSWORD) as mailbox:
            mailbox.folder.set('Отправленные')
            for mail in mails:
                criteria = AND(sent_date_gte=start_finish_days[0].date(),
                               sent_date_lt=start_finish_days[1].date(),
                               text="гривен",
                               to=mail)
                for msg in mailbox.fetch(criteria, charset = 'utf-8'):
                    self.message_list.append([msg.uid, str(msg.date), msg.to, msg.text])
        return self.message_list