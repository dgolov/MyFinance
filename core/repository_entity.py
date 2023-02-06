from MyFinance.models import Expense, Income, Currency, Category, Account
from MyFinance.schemas import CreateCategory, CreateCurrency, CreateAccount, CreateFinanceList
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
    def _filter_by_date(self, result, start_date: datetime = None, end_date: datetime = None):
        pass

    def _amount_sum(self, obj, start_date: datetime = None, end_date: datetime = None):
        result = self.db.query(func.sum(obj.amount).label("total")).all()
        return result


class IncomeEntity(FinanceEntityBase):
    def get_income_list(self, start_date: datetime = None, end_date: datetime = None):
        return self._all(Income)

    def get_income_sum(self, start_date: datetime = None, end_date: datetime = None):
        return self._amount_sum(Income)

    def create(self, data: CreateFinanceList):
        income = Income(**data.dict())
        return self._add(data=income)

    def get_income_by_id(self, pk):
        return self._filter_by_id(obj=Income, pk=pk)


class ExpenseEntity(FinanceEntityBase):
    def get_expense_list(self, start_date: datetime = None, end_date: datetime = None):
        return self._all(Expense)

    def get_expense_sum(self, start_date: datetime = None, end_date: datetime = None):
        return self._amount_sum(Expense)

    def create(self, data: CreateFinanceList):
        expense = Expense(**data.dict())
        return self._add(data=expense)

    def get_expense_by_id(self, pk):
        return self._filter_by_id(obj=Expense, pk=pk)


class CurrencyEntity(Base):
    def get_currency_list(self):
        return self._all(Currency)

    def create(self, data: CreateCurrency):
        currency = Currency(**data.dict())
        return self._add(data=currency)

    def get_currency_by_id(self, pk):
        return self._filter_by_id(obj=Currency, pk=pk)


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

    def create(self, data: Account):
        account = Expense(**data.dict())
        return self._add(data=account)

    def get_account_by_id(self, pk):
        return self._filter_by_id(obj=Account, pk=pk)
