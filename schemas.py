from datetime import date
from pydantic import BaseModel


class Category(BaseModel):
    name: str
    category_type: str


class Income(BaseModel):
    title: str
    category: Category
    company: str = None
    amount: float
    date: date


class Expense(BaseModel):
    title: str
    category: Category
    person: str = None
    amount: float
    date: date
