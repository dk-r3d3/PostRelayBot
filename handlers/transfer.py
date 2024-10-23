import logging
from telethon import events
from aiogram import types, Router

from config import client
from database.views import all_sources, get_recipient

from utils.support import get_channel_id

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

router_transfer = Router()

SOURCE = 0
KEY_WORD = 1

handlers = {}


@router_transfer.callback_query(lambda c: c.data == 'start_transfer')
async def start_transfer(callback_query: types.CallbackQuery):
    sources = await all_sources(callback_query.from_user.id)
    recipient = await get_recipient(callback_query.from_user.id)
    user_id = callback_query.from_user.id

    for source in sources:
        if source[KEY_WORD] != 'None':
            await start_transfer_monitoring_key_word(recipient, source[SOURCE], source[KEY_WORD], user_id)
        if source[KEY_WORD] == "None":
            await start_transfer_monitoring(recipient, source[SOURCE], user_id)

    await callback_query.answer('Monitoring started')


async def start_transfer_monitoring_key_word(recipient, source, key_word, user_id):
    if source not in handlers:
        handlers[user_id] = []  # Инициализируем список получателей для данного канала

        @client.on(events.NewMessage(chats=source))
        async def handler(event):
            try:
                key_words = key_word.split(', ')
                # Проверяем, содержится ли хотя бы одно из ключевых слов в сообщении
                if any(word in event.message.text.lower() for word in key_words):
                    rec_id = await get_channel_id(client, recipient)  # для пересылки
                    if event.message.media:
                        # Пересылаем сообщение с медиа
                        await client.send_message(entity=rec_id,
                                                  message=f"Новый пост в {source}: {event.message.text}",
                                                  file=event.message.media, link_preview=False)
                    else:
                        # Пересылаем текстовое сообщение
                        await client.send_message(entity=rec_id,
                                                  message=f"Новый пост в {source}: {event.message.text}",
                                                  link_preview=False)
            except Exception as error:
                print(f"Exception: {error}\nType: {type(error)}")

        handlers[user_id].append(handler)
        logger.info("start_transfer_monitoring_key_word - Начинаем мониторинг для handlers: %s", handlers)


async def start_transfer_monitoring(recipient, source, user_id):
    if source not in handlers:
        handlers[user_id] = []  # Инициализируем список получателей для данного канала

        @client.on(events.NewMessage(chats=source))
        async def handler(event):
            try:
                rec_id = await get_channel_id(client, recipient)  # для пересылки
                if event.message.media:
                    # Пересылаем сообщение с медиа
                    await client.send_message(entity=rec_id,
                                              message=f"Новый пост в {source}: {event.message.text}",
                                              file=event.message.media,
                                              link_preview=False)
                else:
                    # Пересылаем текстовое сообщение
                    await client.send_message(entity=rec_id,
                                              message=f"Новый пост в {source}: {event.message.text}",
                                              link_preview=False)
            except Exception as error:
                print(f"Exception: {error}\nType: {type(error)}")

        handlers[user_id].append(handler)
        logger.info("start_transfer_monitoring - Начинаем мониторинг для handlers: %s", handlers)


async def stop_transfer_monitoring(user_id):
    """Прекращение мониторинга путем остановки и удаления всех состояний"""
    try:
        handlers_user = handlers[user_id]
        logger.info("stop_transfer_monitoring - handlers_user : %s", handlers_user)
        for handler in handlers_user:
            logger.info("stop_transfer_monitoring - handler : %s", handlers)
            client.remove_event_handler(handler)
            del handlers[user_id]
    except Exception as E:
        logger.info("stop_transfer_monitoring - состояний не было : %s")