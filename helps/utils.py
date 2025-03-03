import re
from collections import defaultdict

from config import mail_and_name


def create_list_summ(temp_list: list) -> list:
    list_summ:list = []
    for msg in temp_list:
        money = re.search(r'\d{2,}', msg[3].split('гривен')[0])
        list_summ.append([msg[2][0], int(money.group())])
    return list_summ

'''Create dictionary for output'''
def create_output(data: list) -> dict:
    result: dict = defaultdict(lambda: [[], 0])
    for email, amount in data:
        result[email][0].append(amount)
        result[email][1] += amount
    return {mail_and_name.get(email): [values[0], values[1]] for email, values in result.items()}

'''Create format output for telegram'''
def format_output_translate(data: dict) -> str:
    return ''.join(
        f'<b><u>{office} </u></b>\n Суммы за период:  {str(money[0])[1:-1]}\n '
        f'Итоговая сумма за период:  <b><i>{money[1]}</i></b>\n'
        for office, money in data.items()
    )