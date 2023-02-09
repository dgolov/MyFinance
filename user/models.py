from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, DateTime, Float, ForeignKey, Boolean
from sqlalchemy.orm import relationship

Base = declarative_base()


class User(Base):
    """ Модель пользователя
    """
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True, unique=True, autoincrement=True)
    name = Column(String, unique=True)
    email = Column(String, unique=True)
    password = Column(String)
    created_at = Column(DateTime)
