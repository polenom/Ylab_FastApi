from sqlalchemy import Column, String, Integer, DateTime

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

SQLALCHEMY_DATABASE_URL = "postgresql://fastapi:fastapi@127.0.0.1:5444/ylab"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

Base = declarative_base()


class Menu(Base):
    __tablename__ = "menu_menu"

    id = Column(Integer, primary_key=True, index=True, unique=True)
    title = Column(String(50))
    description = Column(String(300))
