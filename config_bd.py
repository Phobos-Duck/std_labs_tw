from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_async_engine, update
from sqlalchemy.ext.declarative import declarative_base
from models import TelegramUser
from config_env import get_token

user = get_token("BD_USER")
host = get_token("BD_SERVER")
name_bd = get_token("BD_NAME")
password = get_token("BD_PASS")
engine = create_async_engine(f"mysql+aiomysql://{user}@{host}/{name_bd}", echo=True, pool_size=5, max_overflow=10)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()


async def add_telegram_user(user_id, user_name):
    user_check = session.query(TelegramUser).filter_by(id=user_id).first()
    if user_check:
        user_check.name = user_name
    else:
        new_user_id = TelegramUser(id=user_id)
        session.add(new_user_id)
        new_user_id.name = user_name
    session.commit()


async def add_cmd(current_cmd, user_id):
    user_check = session.query(TelegramUser).filter_by(id=user_id).first()
    user_check.current_cmd = current_cmd
    session.commit()


async def add_city(city, user_id):
    user_check = session.query(TelegramUser).filter_by(id=user_id).first()
    user_check.set_city = city
    session.commit()


async def add_category(category, user_id):
    user_check = session.query(TelegramUser).filter_by(id=user_id).first()
    user_check.set_category = category
    session.commit()

async def check_cc(city, category, user_id):
    result = session.query(TelegramUser.set_city, TelegramUser.set_category).filter_by(id=user_id).first()
    if result:
        city = result.set_city
        category = result.set_category
        return city, category
    else:
        return None, None

async def delete_set(user_id):
    update_bd = (update(TelegramUser).where(TelegramUser.id == user_id).values(set_city=None, set_category=None))
    session.execute(update_bd)
    session.commit()