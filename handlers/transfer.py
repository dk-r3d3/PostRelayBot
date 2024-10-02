from telethon import events
from aiogram import types, Router

from config import client
from database.views import all_couples, get_black_list
from collections import defaultdict

from utils.support import get_channel_id

router_transfer = Router()

"""Индексы в списках"""
SOURСE = 0
RECIPIENT = 1
KEY_WORD = 2

handlers = defaultdict(list)


@router_transfer.callback_query(lambda c: c.data == 'start_transfer')
async def start_transfer(callback_query: types.CallbackQuery):
    res = await all_couples(callback_query.from_user.id)

    for couples in res:
        if couples[KEY_WORD] != 'None':
            await start_transfer_monitoring_key_word(couples, couples[SOURСE], callback_query.from_user.id)
        if couples[KEY_WORD] == "None":
            await start_transfer_monitoring(couples, couples[SOURСE], callback_query.from_user.id)

    await callback_query.answer('Monitoring started')


async def start_transfer_monitoring_key_word(couples, channel, user_id):
    if channel not in handlers:
        @client.on(events.NewMessage(chats=channel))
        async def handler(event):
            try:
                current_black_list = await get_black_list(user_id)
                """Проверяем, есть ли в сообщении слова из черного списка"""
                if any(word in event.message.text.lower() for word in current_black_list):
                    print("Message contains blacklisted words!")
                    return
                else:
                    if couples[KEY_WORD] in event.message.text:
                        rec_id = await get_channel_id(client, couples[RECIPIENT])  # для пересылки
                        if event.message.media:
                            # Пересылаем сообщение с медиа
                            await client.send_message(entity=rec_id,
                                                      message=f"Новый пост в {channel}: {event.message.text}",
                                                      file=event.message.media, link_preview=False)
                        else:
                            # Пересылаем текстовое сообщение
                            await client.send_message(entity=rec_id,
                                                      message=f"Новый пост в {channel}: {event.message.text}",
                                                      link_preview=False)
            except Exception as error:
                print(f"Exception: {error}\nType: {type(error)}")

        handlers[channel].append(handler)


async def start_transfer_monitoring(couples, channel, user_id):
    if channel not in handlers:
        @client.on(events.NewMessage(chats=channel))
        async def handler(event):
            try:
                # Проверяем, нет ли запрещенных слов
                current_black_list = await get_black_list(user_id)
                if any(word in event.message.text.lower() for word in current_black_list):
                    print("Message contains blacklisted words!")
                    return
                else:
                    rec_id = await get_channel_id(client, couples[RECIPIENT])  # для пересылки
                    if event.message.media:
                        # Пересылаем сообщение с медиа
                        await client.send_message(entity=rec_id,
                                                  message=f"Новый пост в {channel}: {event.message.text}",
                                                  file=event.message.media,
                                                  link_preview=False)
                    else:
                        # Пересылаем текстовое сообщение
                        await client.send_message(entity=rec_id,
                                                  message=f"Новый пост в {channel}: {event.message.text}",
                                                  link_preview=False)
            except Exception as error:
                print(f"Exception: {error}\nType: {type(error)}")

        handlers[channel] = [handler]
        print(handlers)
