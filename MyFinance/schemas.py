from datetime import datetime
from pydantic import BaseModel, Field, root_validator


class Category(BaseModel):
    """ Категория доходов и рассходов
    """
    name: str
    category_type: str


class BaseFinance(BaseModel):
    """ Базовый класс доходов и рассходов
    """
    title: str
    category: Category
    amount: float = Field(..., gt=0)
    date: datetime = Field(default_factory=datetime.now)


class Income(BaseFinance):
    """ Доходы
    """
    company: str = None


class Expense(BaseFinance):
    """ Расходы
    """
    person: str = None


class Currency(BaseModel):
    """ Валюта (рубли, доллары, евро и тд)
    """
    name: str


class Account(BaseModel):
    """ Счета
    """
    name: str
    currency: Currency
    updated_at: datetime = datetime.now()
    amount: float
    add_to_balance: bool = True

    class Config:
        validate_assignment = True

    @root_validator
    def update(cls, values):
        values["updated_at"] = datetime.now()
        return values
