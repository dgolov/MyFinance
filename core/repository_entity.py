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

    def _filter_by_id(self, obj, pk):
        result = self.db.query(obj).filter_by(id=pk)
        return self._first(result)

    @staticmethod
    def _first(result):
        return result.first()

    @staticmethod
    def _one(result):
        return result.one()

    def _count(self, obj):
        return len(self.db.query(obj).scalars().all())

    def _add(self, data):
        self.db.add(data)
        self.db.commit()
        self.db.refresh(data)
        return data


class FinanceEntityBase(Base):
    def filter_by_date(self, result, start_date: datetime = None, end_date: datetime = None):
        pass

    def amount_sum(self, obj, start_date: datetime = None, end_date: datetime = None):
        result = self.db.query(func.sum(obj.amount).label("total")).all()
        return result


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

    def get_category_by_id(self, pk):
        return self._filter_by_id(obj=Category, pk=pk)


class AccountEntity(Base):
    def get_account_list(self):
        return self._all(Account)

    def det_account_count(self):
        return self._count(Account)
