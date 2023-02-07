from MyFinance.models import Expense, Income, Currency, Category, Account
from MyFinance.schemas import CreateCategory, CreateCurrency, CreateAccount, CreateFinance
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from typing import Union


class Base:
    """ Базовый класс обращения в БД
    """
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

    @staticmethod
    def _count(result):
        return len(result)

    def _add(self, data):
        self.db.add(data)
        self.db.commit()
        self.db.refresh(data)
        return data


class FinanceEntityBase(Base):
    """ Базобый класс обращения к БД для доходов / расходов
    """
    def _filter_by_date(self, obj, start_date: Union[datetime, None], end_date: Union[datetime, None]):
        """ Фильтр доходов / расходов по датам
        :param obj: Модель расхода / дохода
        :param start_date: Начальная дата
        :param end_date: Конечныя дата
        :return: Ответ БД
        """
        query = self.__get_query_with_filter_by_date(obj, start_date, end_date)
        return query.all()

    def _filter_by_category_id(
            self, obj, start_date: Union[datetime, None], end_date: Union[datetime, None], category_id: int
    ):
        """ Фильтр доходов / расходов по датам
        :param obj: Модель расхода / дохода
        :param category_id: Id категории
        :return: Ответ БД
        """
        query = self.__get_query_with_filter_by_date(obj, start_date, end_date)
        return query.filter_by(category_id=category_id)

    def _amount_sum(self, obj, start_date: Union[datetime, None], end_date: Union[datetime, None]):
        """ Сумма расходов / доходов
        :param obj: Модель расхода / дохода
        :param start_date: Начальная дата
        :param end_date: Конечная дата
        :return: Ответ БД
        """
        result = self.db.query(func.sum(obj.amount).label("total_sum")).\
            filter(obj.date >= start_date, obj.date <= end_date).first()
        return result[0]

    def __get_query_with_filter_by_date(self, obj, start_date: Union[datetime, None], end_date: Union[datetime, None]):
        """ Добавление фильтра по датам в запрос
        :param obj: Модель расхода / дохода
        :param start_date: Начальная дата
        :param end_date: Конечныя дата
        :return: SQL запрос
        """
        query = self.db.query(obj)

        if start_date:
            query = query.filter(obj.date >= start_date)
        if end_date:
            query = query.filter(obj.date <= end_date)

        return query


class IncomeEntity(FinanceEntityBase):
    """Обращение к БД доходов """
    def get_income_list(self, start_date: Union[datetime, None], end_date: Union[datetime, None]):
        if start_date or end_date:
            return self._filter_by_date(Income, start_date, end_date)
        return self._all(Income)

    def get_income_sum(self, start_date: datetime, end_date: datetime):
        return self._amount_sum(Income, start_date, end_date)

    def create(self, data: CreateFinance):
        income = Income(**data.dict())
        account = self._first(result=self.db.query(Account).filter_by(id=income.account_id))
        account.amount += income.amount
        self.db.add(income)
        self.db.add(account)
        self.db.commit()
        self.db.refresh(income)
        return income

    def get_income_by_id(self, pk):
        return self._filter_by_id(obj=Income, pk=pk)


class ExpenseEntity(FinanceEntityBase):
    """Обращение к БД расходов """
    def get_expense_list(self, start_date: Union[datetime, None], end_date: Union[datetime, None]):
        if start_date or end_date:
            return self._filter_by_date(Expense, start_date, end_date)
        return self._all(Expense)

    def get_expense_sum(self, start_date: datetime, end_date: datetime):
        return self._amount_sum(Expense, start_date, end_date)

    def create(self, data: CreateFinance):
        print(data)
        expense = Expense(**data.dict())
        account = self._first(result=self.db.query(Account).filter_by(id=expense.account_id))
        account.amount -= expense.amount
        self.db.add(expense)
        self.db.add(account)
        self.db.commit()
        self.db.refresh(expense)
        return expense

    def get_expense_by_id(self, pk):
        return self._filter_by_id(obj=Expense, pk=pk)


class CurrencyEntity(Base):
    """Обращение к БД валют """
    def get_currency_list(self):
        return self._all(Currency)

    def create(self, data: CreateCurrency):
        currency = Currency(**data.dict())
        return self._add(data=currency)

    def get_currency_by_id(self, pk):
        return self._filter_by_id(obj=Currency, pk=pk)


class CategoryEntity(Base):
    """Обращение к БД категорий """
    def get_category_list(self):
        return self._all(Category)

    def det_category_count(self):
        result = self._all(Category)
        return self._count(result)

    def create(self, data: CreateCategory):
        category = Category(**data.dict())
        return self._add(data=category)

    def get_category_by_id(self, pk):
        return self._filter_by_id(obj=Category, pk=pk)


class AccountEntity(Base):
    """Обращение к БД счетов """
    def get_account_list(self):
        return self._all(Account)

    def det_account_count(self):
        result = self._all(Account)
        return self._count(result)

    def create(self, data: CreateAccount):
        account = Account(**data.dict())
        return self._add(data=account)

    def get_account_by_id(self, pk):
        return self._filter_by_id(obj=Account, pk=pk)

    def get_account_sum(self):
        result = self._first(self.db.query(func.sum(Account.amount).label("total")).filter_by(add_to_balance=True))
        return result[0]
