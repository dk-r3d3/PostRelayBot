import os

from aiogram import Bot
from telethon import TelegramClient
from dotenv import load_dotenv

load_dotenv()  # Загружаем переменные из .env

BOT_TOKEN = os.getenv('BOT_TOKEN')
API_ID = os.getenv('API_ID')
API_HASH = os.getenv('API_HASH')
DATABASE_URL = os.getenv('DATABASE_URL')


bot = Bot(token=BOT_TOKEN)
client = TelegramClient('session_from_education', int(API_ID), API_HASH)
