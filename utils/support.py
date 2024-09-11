
async def get_channel_id(client, channel_name):
    """Функция для получения id канала"""
    entity = await client.get_entity(channel_name)
    return entity.id


async def check_channel_exists(client, channel_name):
    try:
        res = await client.get_input_entity(channel_name)
        return True
    except Exception as e:
        return False
