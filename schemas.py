from datetime import datetime
from pydantic import BaseModel, Field


class Category(BaseModel):
    name: str
    category_type: str


class BaseFinance(BaseModel):
    title: str
    category: Category
    amount: float = Field(..., gt=0)
    date: datetime = Field(default_factory=datetime.now)


class Income(BaseFinance):
    company: str = None


class Expense(BaseFinance):
    person: str = None
