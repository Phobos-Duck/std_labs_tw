from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from config_env import get_token

Base = declarative_base()
name_table = get_token("BD_TABLE")

class TelegramUser(Base):
    __tablename__ = f'{name_table}'
    id = Column(Integer, primary_key=True)
    name = Column(String, primary_key=True)
    current_cmd = Column(String, primary_key=True)
    set_city = Column(String, primary_key=True)
    set_category = Column(String, primary_key=True)