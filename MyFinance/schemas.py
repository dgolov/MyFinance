from datetime import datetime
from pydantic import BaseModel, Field, root_validator
from typing import List


class CurrencyBase(BaseModel):
    """ Базовый класс сериализации валюты
    """
    name: str

    class Config:
        orm_mode = True


class CurrencySchema(CurrencyBase):
    """ Список валют (рубли, доллары, евро и тд)
    """
    id: int


class CreateCurrency(CurrencyBase):
    """ Создане валют (рубли, доллары, евро и тд)
    """
    pass


class AccountBase(BaseModel):
    """ Базовый класс сериализации счетов
    """
    name: str
    amount: float
    add_to_balance: bool = True

    class Config:
        orm_mode = True


class AccountSchema(AccountBase):
    """ Список счетов
    """
    id: int
    updated_at: datetime
    currency: CurrencySchema


class CreateAccount(AccountBase):
    """ Создание счета
    """
    currency_id: int

    class Config:
        validate_assignment = True

    @root_validator(pre=True, skip_on_failure=True)
    def update(cls, values):
        values["updated_at"] = datetime.utcnow()
        return values


class CategoryBase(BaseModel):
    """ Базовый класс сериализации категорий
    """
    name: str
    category_type: str

    class Config:
        orm_mode = True


class CategorySchema(CategoryBase):
    """ Список категорий доходов и рассходов
    """
    id: int


class CreateCategory(CategoryBase):
    """ Создание категорий доходов и рассходов
    """
    pass


class BaseFinance(BaseModel):
    """ Базовый класс доходов и рассходов
    """
    title: str
    amount: float = Field(..., gt=0)

    class Config:
        orm_mode = True


class BaseFinanceSchema(BaseFinance):
    """ Базовый класс списков доходов и рассходов
    """
    id: int
    category: CategorySchema
    account: AccountSchema
    date: datetime


class IncomeSchema(BaseFinanceSchema):
    """ Список доходов
    """
    pass


class ExpenseSchema(BaseFinanceSchema):
    """ Список расходов
    """
    pass


class CreateFinance(BaseFinance):
    """ Создание доходов и рассходов
    """
    category_id: int
    account_id: int


class AccountSumSchema(BaseModel):
    currency: str = "USD"
    amount: float = 1000


class MainSchema(BaseModel):
    """ Серилизация главной строницы
    """
    account_sum: List[AccountSumSchema]
    income: List[IncomeSchema]
    expense: List[ExpenseSchema]
