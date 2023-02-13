from datetime import datetime
from sqlalchemy import Column, String, Integer, DateTime, Float, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from core.engine import Base


class Currency(Base):
    """ Модель валют (рубли, доллары, евро и тд)
    """
    __tablename__ = "currency"

    id = Column(Integer, primary_key=True, index=True, unique=True, autoincrement=True)
    name = Column(String)


class Account(Base):
    """ Модель счетов
    """
    __tablename__ = "account"

    id = Column(Integer, primary_key=True, index=True, unique=True, autoincrement=True)
    name = Column(String)
    currency_id = Column(Integer, ForeignKey('currency.id'))
    currency = relationship("Currency", lazy="joined")
    updated_at = Column(DateTime)
    amount = Column(Float)
    add_to_balance = Column(Boolean, default=True)


class Category(Base):
    """ Модель категорий доходов и рассходов
    """
    __tablename__ = "category"

    id = Column(Integer, primary_key=True, index=True, unique=True, autoincrement=True)
    name = Column(String)
    category_type = Column(String)


class Income(Base):
    """ Модель доходов
    """
    __tablename__ = "income"

    id = Column(Integer, primary_key=True, index=True, unique=True, autoincrement=True)
    title = Column(String)
    category_id = Column(Integer, ForeignKey('category.id'))
    category = relationship("Category", lazy="joined")
    amount = Column(Float)
    account_id = Column(Integer, ForeignKey('account.id'))
    account = relationship("Account", lazy="joined")
    date = Column(DateTime, default=datetime.utcnow())


class Expense(Base):
    """ Модель расходов
    """
    __tablename__ = "expense"

    id = Column(Integer, primary_key=True, index=True, unique=True, autoincrement=True)
    title = Column(String)
    category_id = Column(Integer, ForeignKey('category.id'))
    category = relationship("Category", lazy="joined")
    amount = Column(Float)
    account_id = Column(Integer, ForeignKey('account.id'))
    account = relationship("Account", lazy="joined")
    date = Column(DateTime, default=datetime.utcnow())
