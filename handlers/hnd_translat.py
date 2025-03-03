import logging.config

from aiogram import F, Router
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from config import days, months, names
from dialogs import replicas
from helps.utils import format_output_translate
from keyboards.kb_translate import (button_days, button_months, buttons_office,
                                    buttons_translate)
from keyboards.kbd_main import buttons_main
from offices_translate import MoneyForMonth, MoneyForPeriod
from states_translate.states import Month, Period
from logging_config import LOGGING_CONFIG

router_transl = Router()
period_agency = []
logging.config.dictConfig(LOGGING_CONFIG)
error_logger = logging.getLogger('log_error')
debug_logger = logging.getLogger('log_debug')
info_logger = logging.getLogger('log_info')

# Check translate
@router_transl.message(F.text == replicas["translate"])
async def translate(message: Message, state: FSMContext):
    await message.answer(text=replicas["month_or_period"], reply_markup=buttons_translate())
    await state.set_state(Month.choosing_month)

@router_transl.message(Month.choosing_month, F.text == replicas["month"])
async def month(message: Message):
    await message.answer(text=replicas["select_month"], reply_markup=button_months())

# если выбран расчет по периоду версия 2
@router_transl.message(F.text == replicas["period_agency"])
async def period_and_agency(message: Message, state: FSMContext):
    await message.answer(text=replicas["select_month"], reply_markup=button_months())
    await state.set_state(Period.choosing_day)

# После выбора месяца, предложение выбрать день вер. 2
@router_transl.message(Period.choosing_day, F.text.in_(months))
async def period_chosen(message: Message, state: FSMContext):
    period_agency.append(message.text)
    await message.answer(text=replicas["message_day"], reply_markup=button_days())
    await state.set_state(Period.choosing_office)

# После выбора дня, предложение выбрать офис вер. 2
@router_transl.message(Period.choosing_office, F.text.in_(days))
async def office_chosen(message: Message, state: FSMContext):
    period_agency.append(message.text)
    await message.answer(text='Пожалуйста введите офис', reply_markup=buttons_office())
    await message.answer(text=replicas["please_wait"])
    await state.set_state(Period.get_mail)

# выбор офиса для версии 2.
@router_transl.message(Period.choosing_period)
async def period_chosen(message: Message, state: FSMContext):
    period_agency.append(message.text)
    await message.answer(text='Пожалуйста введите офис', reply_markup=buttons_office())
    await state.set_state(Period.choosing_office)

# после выбора офиса, расчет и вывод
@router_transl.message(Period.get_mail, F.text.in_(names))
async def get_mail(message: Message, state: FSMContext):
    period_agency.append(message.text)
    period = MoneyForPeriod(period_agency)
    await message.answer(text=replicas["please_wait"])
    summa_dict: dict = period.request_summ()
    zero_message = summa_dict.get('message')
    if not zero_message:
        message_out: str = format_output_translate(summa_dict)
    else:
        message_out: str = zero_message
    await message.answer(text=message_out, reply_markup=buttons_main(), parse_mode=ParseMode.HTML)
    await state.clear()
    period_agency.clear()

@router_transl.message(Month.choosing_month, F.text.in_(months))
async def month_chooses(message: Message, state: FSMContext):
    """ calculation when choosing - 'amount for month'"""
    month_day: list = [message.text, "1"]
    month_ = MoneyForMonth(month_day)
    await message.answer(text=replicas["please_wait"])
    summa_dict: dict = month_.request_summ()
    zero_message = summa_dict.get('message')
    if not zero_message:
        message_out: str = format_output_translate(summa_dict)
    else:
        message_out: str = zero_message
    await message.answer(text=message_out, reply_markup=buttons_main(), parse_mode=ParseMode.HTML)
    await state.clear()