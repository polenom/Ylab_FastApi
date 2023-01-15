from sqlalchemy import Column, String, Integer, ForeignKey, Float, Numeric

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

SQLALCHEMY_DATABASE_URL = "postgresql://fastapi:fastapi@127.0.0.1:5444/ylab"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

Base = declarative_base()


class BaseModel(Base):
    __abstract__ = True

    id = Column(Integer, primary_key=True, index=True, unique=True)
    title = Column(String(50))
    description = Column(String(300))


class Menu(BaseModel):
    __tablename__ = "menu"


class Submenu(BaseModel):
    __tablename__ = "submenu"

    menu_id = Column(
        Integer,
        ForeignKey('menu.id', onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False
    )


class Dish(BaseModel):
    __tablename__ = "dish"

    submenu_id = Column(
        Integer,
        ForeignKey('submenu.id', ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False
    )
    price = Column(Numeric(precision=10, scale=2))