from aiogram import types, Router
from aiogram.filters import Command

from utils.keyboards import start_keyboard
from database.views import add_user, get_recipient
from utils.support import format_channels, menu

router_commands = Router()


@router_commands.message(Command("start"))
async def cmd_start(message: types.Message):
    recipient_channel = await get_recipient(message.from_user.id)
    source_channels = await format_channels(message.from_user.id)

    await menu(message.chat.id, recipient_channel, source_channels, start_keyboard(recipient_channel))
    await add_user(message.from_user.id, message.from_user.username)
