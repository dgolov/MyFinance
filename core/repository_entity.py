from MyFinance.models import Expense, Income, Currency, Category, Account
from MyFinance.schemas import CreateCategory
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy.sql import func


class Base:
    def __init__(self, db: Session):
        self.db = db

    def _all(self, obj):
        return self.db.query(obj).all()

    def _first(self, obj):
        return self.db.query(obj).first()

    def _one(self, obj):
        return self.db.query(obj).one()

    def _count(self, obj):
        return len(self.db.query(obj).scalars().all())

    def _add(self, data):
        self.db.add(data)
        self.db.commit()
        self.db.refresh(data)
        return data


class FinanceEntityBase(Base):
    def amount_sum(self, obj):
        return self.db.query(func.sum(obj.amount).label("total")).all()


class IncomeEntity(FinanceEntityBase):
    def get_income_list(self, date: datetime = None):
        return self._all(Income)


class ExpenseEntity(FinanceEntityBase):
    def get_expense_list(self, date: datetime = None):
        return self._all(Expense)


class CurrencyEntity(Base):
    def get_currency_list(self):
        return self._all(Currency)


class CategoryEntity(Base):
    def get_category_list(self):
        return self._all(Category)

    def det_category_count(self):
        return self._count(Category)

    def create(self, data: CreateCategory):
        category = Category(**data.dict())
        return self._add(data=category)


class AccountEntity(Base):
    def get_account_list(self):
        return self._all(Account)

    def det_account_count(self):
        return self._count(Account)
