import os

from aiogram import Bot
from telethon import TelegramClient
from dotenv import load_dotenv

load_dotenv()  # Загружаем переменные из .env

BOT_TOKEN = os.getenv('BOT_TOKEN')
API_ID = os.getenv('API_ID')
API_HASH = os.getenv('API_HASH')

bot = Bot(token=BOT_TOKEN)
client = TelegramClient('session_from_education', int(API_ID), API_HASH)
DATABASE_URL = "postgresql+asyncpg://postgres:D97794422d69@localhost:5432/transfer_bot"

"""ВРЕМЕННЫЕ РЕШЕНИЯ"""

origin_channels: list = []
recipient_channels: list = []
