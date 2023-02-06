from datetime import datetime
from pydantic import BaseModel, Field, root_validator


class CurrencyBase(BaseModel):
    """ Базовый класс сериализации валюты
    """
    name: str

    class Config:
        orm_mode = True


class CurrencyList(CurrencyBase):
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
    updated_at: datetime
    amount: float
    add_to_balance: bool = True

    class Config:
        orm_mode = True


class AccountList(AccountBase):
    """ Список счетов
    """
    id: int
    currency: CurrencyList


class CreateAccount(AccountBase):
    """ Создание счета
    """
    currency_id: int

    class Config:
        validate_assignment = True

    @root_validator
    def update(cls, values):
        values["updated_at"] = datetime.now()
        return values


class CategoryBase(BaseModel):
    """ Базовый класс сериализации категорий
    """
    name: str
    category_type: str

    class Config:
        orm_mode = True


class CategoryList(CategoryBase):
    """ Список категорий доходов и рассходов
    """
    id: str


class CreateCategory(CategoryBase):
    """ Создание категорий доходов и рассходов
    """
    pass


class BaseFinance(BaseModel):
    """ Базовый класс доходов и рассходов
    """
    title: str
    amount: float = Field(..., gt=0)
    date: datetime = Field(default_factory=datetime.now)

    class Config:
        orm_mode = True


class BaseFinanceList(BaseFinance):
    """ Базовый класс списков доходов и рассходов
    """
    id: int
    category: CategoryList
    account = AccountList


class IncomeList(BaseFinance):
    """ Список доходов
    """
    pass


class ExpenseList(BaseFinance):
    """ Список расходов
    """
    pass


class CreateFinance(BaseFinance):
    """ Создание доходов и рассходов
    """
    category_id: int
    account_id: int
