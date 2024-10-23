from database.views import all_sources
from config import bot


async def get_channel_id(client, channel_name):
    """Функция для получения id канала"""
    entity = await client.get_entity(channel_name)
    return entity.id


async def check_channel_exists(client, channel_name):
    """Проверка на существование канала"""
    try:
        await client.get_input_entity(channel_name)  # получаем сущность объекта
        return True
    except Exception as error:
        print(f"Exception: {error}\nType: {type(error)}")
        return False


async def format_channels(user_id):
    """Данная функция предназначена для преобразования списка в строку"""
    channels = await all_sources(user_id)
    return (
        "\n".join(f"_____\nИсточник - {x}\nКлючевое слово - {w}" for x, w in channels))


async def menu(chat_id, recipient_channel, source_channels, start_keyboard):
    await bot.send_message(chat_id=chat_id,
                           text=f'Канал-получатель: {recipient_channel if recipient_channel is not None else ""}\n'
                                f'Каналы-источники: \n{source_channels}\n',  # добавлять с клоючевыми словами
                           reply_markup=start_keyboard
                           )
