from sqlalchemy import Column, Integer, String, ARRAY
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from config import DATABASE_URL

engine = create_async_engine(DATABASE_URL)
AsyncSessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)

"""
Фабрика сессий для взаимодействия с БД
async_sessionmaker: Это фабрика для создания объектов асинхронных сессий, которые обеспечивают взаимодействие
с базой данных. bind=engine: Связывает сессию с определённым движком (engine), который определяет
подключение к базе данных. engine управляет всеми низкоуровневыми операциями подключения к базе данных.
"""
Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, unique=True, nullable=False)
    username = Column(String, unique=True, nullable=True)


class Recipient(Base):
    __tablename__ = "recipient"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    recipient_channel = Column(String, nullable=False)


class Source(Base):
    __tablename__ = 'sources'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    source_channel = Column(String, nullable=False)
    key_word = Column(String, nullable=True)

    def print_res(self):
        res = [self.source_channel, self.key_word]
        return res


async def init_db():
    async with engine.begin() as conn:
        # Создание таблиц на основе определенных моделей
        await conn.run_sync(Base.metadata.create_all)
