import re
import calendar
import datetime

from imap_tools import MailBox, AND, OR

from offices_translate import MoneyForPeriod

year = 2025
period = MoneyForPeriod(['2', '14', 'Елена'])
print(period.request_email())
