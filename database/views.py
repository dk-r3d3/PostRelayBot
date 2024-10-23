from database.models import AsyncSessionLocal, User, Recipient, Source
from sqlalchemy.future import select
from sqlalchemy import delete, update


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


async def add_recipient(user_id: int, recipient_channel: str):
    async with AsyncSessionLocal() as db:
        db_channel = Recipient(user_id=user_id,
                               recipient_channel=recipient_channel)
        db.add(db_channel)
        await db.commit()
        await db.refresh(db_channel)


async def update_recipient_in_db(user_id: int, recipient_channel_new: str):
    async with AsyncSessionLocal() as db:
        rec = update(Recipient).where(Recipient.user_id == user_id).values(recipient_channel=recipient_channel_new)
        await db.execute(rec)
        await db.commit()


async def add_source(user_id: int, source_channel: str, key_word: str):
    async with AsyncSessionLocal() as db:
        db_channel = Source(user_id=user_id,
                            source_channel=source_channel,
                            key_word=key_word)
        db.add(db_channel)
        await db.commit()
        await db.refresh(db_channel)


async def delete_source(source: str):
    """Delete source"""
    async with AsyncSessionLocal() as db:
        rec = delete(Source).where(Source.source_channel == source)
        await db.execute(rec)
        await db.commit()


async def get_recipient(user_id: int):
    async with AsyncSessionLocal() as db:
        recipient = select(Recipient.recipient_channel).where(Recipient.user_id == user_id)
        result = await db.execute(recipient)
        return result.scalars().first()


async def all_sources(user_id: int):
    """Get all sources"""
    async with AsyncSessionLocal() as db:
        try:
            source = select(Source.source_channel).where(Source.user_id == user_id)
            key_words = select(Source.key_word).where(Source.user_id == user_id)
            result1 = await db.execute(source)
            result2 = await db.execute(key_words)
            channels1 = result1.scalars().all()
            key_word = result2.scalars().all()
            return [[s, w] for s, w in zip(channels1, key_word)]
        except Exception as error:
            print(f"Exception: {error}\nType: {type(error)}")
