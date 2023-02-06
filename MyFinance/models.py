from core.engine import Base
from sqlalchemy import Column, String, Integer, DateTime, Float, ForeignKey, Boolean


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
    updated_at = Column(DateTime)
    amount = Column(Float)
    add_to_balance = Column(Boolean)


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
    amount = Column(Float)
    account_id = Column(Integer, ForeignKey('account.id'))
    date = Column(DateTime)
    company = Column(String)


class Expense(Base):
    """ Модель расходов
    """
    __tablename__ = "expense"

    id = Column(Integer, primary_key=True, index=True, unique=True, autoincrement=True)
    title = Column(String)
    category_id = Column(Integer, ForeignKey('category.id'))
    amount = Column(Float)
    account_id = Column(Integer, ForeignKey('account.id'))
    date = Column(DateTime)
    person = Column(String)