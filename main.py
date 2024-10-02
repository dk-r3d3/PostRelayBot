import asyncio
import logging

from aiogram import Dispatcher

from config import bot, client
from handlers.commands import router_commands
from handlers.channels import router_channels
from handlers.transfer import router_transfer

from database.models import init_db

logging.basicConfig(level=logging.INFO)


async def main():

    dp = Dispatcher()

    dp.include_routers(router_commands, router_channels, router_transfer)
    await init_db()  # создали таблицы
    await client.start()
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
