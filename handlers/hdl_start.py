import json
from json import JSONDecodeError

import aiofiles
from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from dialogs import replicas
from keyboards.kb_plan import buttons_plan
from keyboards.kbd_main import buttons_main
from states_translate.states import Main

router_start = Router()
Users = {}
async def load_users():
    async with aiofiles.open('Users.json', mode='r') as file:
        contents = await file.read()
        try:
            users = json.loads(contents)
        except JSONDecodeError:
            users = {}
        return users

async def write_users(user):
    async with aiofiles.open('Users.json', mode='w') as file:
        await file.write(json.dumps(user, ensure_ascii=False))


@router_start.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    users_loaded = await load_users()
    user_id = message.from_user.id
    if user_id in users_loaded.values():
        if user_id == 1346260273:
            await message.answer(replicas["hello_admin"], reply_markup=buttons_main())
        else:
            await message.answer(replicas["select_action"], reply_markup=buttons_plan())
    else:
        await message.answer(replicas["hello"])
        await state.set_state(Main.name)

@router_start.message(Main.name, F.text)
async def name(message:Message, state: FSMContext):
    Users[message.text] = message.from_user.id
    await write_users(Users)
    if message.from_user.id == 1346260273:
        await message.answer(replicas["hello_admin"],reply_markup=buttons_main())
    else:
        await message.answer(replicas["registration_ok"],reply_markup=buttons_plan())
    await state.clear()