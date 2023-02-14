from datetime import datetime
from pydantic import BaseModel, Field, root_validator


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
    user_id: int


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
    user_id: int

    class Config:
        validate_assignment = True

    @root_validator
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
    user_id: int


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
    user_id: int
