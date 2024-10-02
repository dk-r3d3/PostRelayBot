from database.views import all_couples, get_black_list


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
    channels = await all_couples(user_id)
    return ("Список каналов:\n" +
            "\n".join(f"_____\nИсточник - {x}\nПолучатель - {y}\nКлючевое слово - {w}" for x, y, w in channels))


async def format_black_list(user_id):
    """Данная функция предназначена для преобразования списка в строку"""
    black_list = await get_black_list(user_id)
    return f"Черный список слов: {', '.join(str(x) for x in black_list)}"
