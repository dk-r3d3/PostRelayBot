from aiogram import types, Router
from aiogram.filters import Command

from utils.keyboards import start_keyboard
from database.views import add_user, get_all_channels

router_commands = Router()


@router_commands.message(Command("start"))
async def cmd_start(message: types.Message):
    channels = await get_all_channels(message.from_user.id)
    await message.answer_sticker(sticker='CAACAgIAAxkBAAEMVc9mcYyLzy-L47I3HobT3NVw_KJ4PAACrQkAAnlc4gnGTO4AAVwKVRo1BA')
    await message.answer(
        text=f'Привет, данный бот предназначен для пересылки постов из указанных телеграм-каналов '
             f'в целевые телеграм-каналы, а так же тебе в личные сообщения.'
             f'Пересылка возможна по ключевым словам!'
             f'Ваши пары каналов-источников и каналов-получателей:\n {channels}',
        reply_markup=start_keyboard()
    )
    await add_user(message.from_user.id, message.from_user.username)
