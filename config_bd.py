from sqlalchemy.orm import sessionmaker
from sqlalchemy import update
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.future import select
from models import TelegramUser
from config_env import get_token

user = get_token("BD_USER")
host = get_token("BD_SERVER")
name_bd = get_token("BD_NAME")
#password = get_token("BD_PASS")
engine = create_async_engine(f"mysql+aiomysql://{user}@{host}/{name_bd}", echo=True, pool_size=5, max_overflow=10)
# в случае, если есть пароль, раскомитить вот эту строку вместе с password и занести в token.env (в BD_PASS) пароль от бд:
#engine = create_async_engine(f"mysql+aiomysql://{user}:{password}@{host}/{name_bd}", echo=True, pool_size=5, max_overflow=10)

async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
Base = declarative_base()


async def add_telegram_user(_id, user_name):
    async with async_session() as conn:
            user_check = await conn.execute(select(TelegramUser).filter_by(id=_id))
            existing_user = user_check.fetchone()
            if existing_user:
                existing_user[0].name = user_name
            else:
                new_user_id = TelegramUser(id=_id)
                conn.add(new_user_id)
                new_user_id.name = user_name
            await conn.commit()


async def add_cmd(cmd, _id):
    async with async_session() as conn:
        user_check = await conn.execute(select(TelegramUser).filter_by(id=_id))
        existing_user = user_check.fetchone()
        if existing_user:
            existing_user[0].current_cmd = cmd
            await conn.commit()


async def add_city(city, user_id):
    async with async_session() as conn:
        user_check = await conn.execute(select(TelegramUser).filter_by(id=user_id))
        existing_user = user_check.fetchone()
        if existing_user:
            existing_user[0].set_city = str(city)
            await conn.commit()


async def add_category(category, user_id):
    async with async_session() as conn:
        user_check = await conn.execute(select(TelegramUser).filter_by(id=user_id))
        existing_user = user_check.fetchone()
        if existing_user:
            existing_user[0].set_category = category
            await conn.commit()


async def check_cc(city, category, user_id):
    async with async_session() as conn:
        result = await conn.execute(select(TelegramUser.set_city, TelegramUser.set_category).filter_by(id=user_id))
        existing = result.fetchone()
        if existing:
            city = existing[0]
            category = existing[1]
            return city, category
        else:
            return None, None


async def delete_set(user_id):
    async with async_session() as conn:
        await conn.execute(update(TelegramUser).where(TelegramUser.id == user_id).values(set_city=None, set_category=None))
        await conn.commit()