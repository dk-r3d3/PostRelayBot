from telethon import events
from aiogram import types, Router
import asyncio

from config import bot, client
from database.views import all_couples

"""Временно"""
from utils.support import get_channel_id

router_transfer = Router()

SOURСE = 0
RECIPIENT = 1
KEY_WORD = 2


@router_transfer.callback_query(lambda c: c.data == 'start_transfer')
async def start_transfer(callback_query: types.CallbackQuery):
    res = await all_couples(callback_query.from_user.id)
    for couples in res:
        if couples[KEY_WORD] != 'None':
            # rec_id = await get_channel_id(client, couples[SOURСE])  # ущетсвует ли канал????
            await start_transfer_monitoring_key_word(couples, couples[SOURСE])
        if couples[KEY_WORD] == "None":
            # rec_id = await get_channel_id(client, couples[SOURСE])  # ущетсвует ли канал????
            await start_transfer_monitoring(couples, couples[SOURСE])

    await callback_query.answer('Monitoring started')


async def start_transfer_monitoring_key_word(couples, channel):
    @client.on(events.NewMessage(chats=channel))
    async def handler(event):
        try:
            if couples[KEY_WORD] in event.message.text:
                rec_id = await get_channel_id(client, couples[RECIPIENT])
                await client.send_message(entity=rec_id, message=f"Новый пост в {channel}: {event.message.text}")
        except ValueError as val:
            print("fuck you")


async def start_transfer_monitoring(couples, channel):
    @client.on(events.NewMessage(chats=channel))
    async def handler(event):
        try:
            rec_id = await get_channel_id(client, couples[RECIPIENT])
            await client.send_message(entity=rec_id, message=f"Новый пост в {channel}: {event.message.text}")
        except ValueError as val:
            print("fuck you")
