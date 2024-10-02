from database.models import AsyncSessionLocal, User, Channel, BlackList
from sqlalchemy.future import select
from sqlalchemy import delete


async def add_user(user_id: int, username: str):
    """Add user to the database"""
    async with AsyncSessionLocal() as db:
        try:
            db_user = User(user_id=user_id, username=username)
            db.add(db_user)
            await db.commit()
            await db.refresh(db_user)
            return db_user
        except Exception as error:
            print(f"Exception: {error}\nType: {type(error)}")


async def add_channels(user_id: int, source_channel: str, recipient_channel: str, key_word: str):
    couples = await all_couples(user_id)

    async with AsyncSessionLocal() as db:
        db_channel = Channel(user_id=user_id,
                             source_channel=source_channel,
                             recipient_channel=recipient_channel,
                             key_word=key_word)
        if db_channel.print_res() not in couples:
            db.add(db_channel)
            await db.commit()
            await db.refresh(db_channel)


async def delete_channels(source: str):
    """Delete couple"""
    async with AsyncSessionLocal() as db:
        rec = delete(Channel).where(Channel.source_channel == source)
        await db.execute(rec)
        await db.commit()


async def all_couples(user_id: int):
    """Get all couples"""
    async with AsyncSessionLocal() as db:
        try:
            source = select(Channel.source_channel).where(Channel.user_id == user_id)
            recipient = select(Channel.recipient_channel).where(Channel.user_id == user_id)
            key_words = select(Channel.key_word).where(Channel.user_id == user_id)
            result1 = await db.execute(source)
            result2 = await db.execute(recipient)
            result3 = await db.execute(key_words)
            channels1 = result1.scalars().all()
            channels2 = result2.scalars().all()
            key_word = result3.scalars().all()
            return [[s, r, w] for s, r, w in zip(channels1, channels2, key_word)]
        except Exception as error:
            print(f"Exception: {error}\nType: {type(error)}")


async def add_black_words(user_id: int, black_word: str):
    async with AsyncSessionLocal() as db:
        try:
            black_word = BlackList(user_id=user_id, black_word=black_word)
            db.add(black_word)
            await db.commit()
            await db.refresh(black_word)
        except Exception as error:
            print(f"Exception: {error}\nType: {type(error)}")


async def get_black_list(user_id: int):
    async with AsyncSessionLocal() as db:
        try:
            black_list_words = select(BlackList.black_word).where(BlackList.user_id == user_id)
            result = await db.execute(black_list_words)
            channels1 = result.scalars().all()
            return [word for word in channels1]
        except Exception as error:
            print(f"Exception: {error}\nType: {type(error)}")


async def delete_black_word_view(word: str):
    async with AsyncSessionLocal() as db:
        rec = delete(BlackList).where(BlackList.black_word == word)
        await db.execute(rec)
        await db.commit()
