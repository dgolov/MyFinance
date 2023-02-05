from datetime import date
from pydantic import BaseModel, validator


class Category(BaseModel):
    name: str
    category_type: str


class BaseFinance(BaseModel):
    title: str
    category: Category
    amount: float
    date: date

    @validator("amount")
    def check_amount(cls, value):
        if value < 0:
            raise ValueError("Argument amount must be more than 0")
        return value


class Income(BaseFinance):
    company: str = None


class Expense(BaseFinance):
    person: str = None
