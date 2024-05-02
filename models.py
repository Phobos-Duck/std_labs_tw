from sqlalchemy import Column, Integer
from sqlalchemy.ext.declarative import declarative_base
from config_env import get_token

Base = declarative_base()
name_table = get_token("BD_TABLE")
class TelegramUser(Base):
    __tablename__ = f'{name_table}'
    id = Column(Integer, primary_key=True)
    name = Column(Integer, primary_key=True)
    current_cmd = Column(Integer, primary_key=True)
    set_city = Column(Integer, primary_key=True)
    set_category = Column(Integer, primary_key=True)