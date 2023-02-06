from datetime import datetime
from pydantic import BaseModel, Field, root_validator


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


class Currency(BaseModel):
    name: str


class Account(BaseModel):
    name: str
    currency: Currency
    updated_at: datetime = datetime.now()
    amount: float

    class Config:
        validate_assignment = True

    @root_validator
    def update(cls, values):
        values["updated_at"] = datetime.now()
        return values
