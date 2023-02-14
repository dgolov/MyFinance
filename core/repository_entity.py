from sqlalchemy import select, insert
from MyFinance.models import Expense, Income, Currency, Category, Account
from MyFinance.schemas import CreateCategory, CreateCurrency, CreateAccount, CreateFinance
from datetime import datetime
from sqlalchemy.sql import func
from typing import Union


class Base:
    """ Базовый класс обращения в БД
    """
    def __init__(self, session):
        self.session = session

    async def _all(self, obj, user_id: int):
        query = select(obj).filter(obj.user_id == user_id)
        result = await self.session.execute(query)
        row = result.all()
        return [data[0] for data in row]

    async def _filter_by_id(self, obj, pk: int):
        query = select(obj).filter(obj.id == int(pk))
        result = await self.session.execute(query)
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

    async def _add(self, obj, data):
        query = insert(obj).values(**data.dict())
        await self.session.execute(query)
        await self.session.commit()
        return {"status": "success"}


class FinanceEntityBase(Base):
    """ Базобый класс обращения к БД для доходов / расходов
    """
    async def _filter_by_date(
            self, obj, user_id: int, start_date: Union[datetime, None], end_date: Union[datetime, None]
    ):
        """ Фильтр доходов / расходов по датам
        :param obj: Модель расхода / дохода
        :param start_date: Начальная дата
        :param end_date: Конечныя дата
        :return: Ответ БД
        """
        return await self.__get_query_with_filter_by_date(obj, user_id, start_date, end_date)

    async def _filter_by_category_id(
            self, obj, start_date: Union[datetime, None], end_date: Union[datetime, None], category_id: int
    ) -> list:
        """ Фильтр доходов / расходов по датам
        :param obj: Модель расхода / дохода
        :param category_id: Id категории
        :return: Ответ БД
        """
        return await self._filter_by_id(obj, start_date, end_date)

    async def _amount_sum(self, obj, start_date: Union[datetime, None], end_date: Union[datetime, None]):
        """ Сумма расходов / доходов
        :param obj: Модель расхода / дохода
        :param start_date: Начальная дата
        :param end_date: Конечная дата
        :return: Ответ БД
        """
        query = select(func.sum(obj.amount).label("total_sum")).\
            filter(obj.date >= start_date, obj.date <= end_date).first()
        result = await self.session.execute(query)
        row = result.first()
        return row[0]

    async def __get_query_with_filter_by_date(
            self, obj, user_id: int, start_date: Union[datetime, None], end_date: Union[datetime, None]
    ):
        """ Добавление фильтра по датам в запрос
        :param obj: Модель расхода / дохода
        :param user_id: Текущий пользователь
        :param start_date: Начальная дата
        :param end_date: Конечныя дата
        :return: SQL запрос
        """
        query = select(obj).filter(obj.user_id == user_id)
        if start_date:
            query = query.filter(obj.date >= start_date)
        if end_date:
            query = query.filter(obj.date <= end_date)

        result = await self.session.execute(query)
        row = result.all()

        return [data[0] for data in row]


class IncomeEntity(FinanceEntityBase):
    """Обращение к БД доходов """
    async def get_income_list(self, user_id: int, start_date: Union[datetime, None], end_date: Union[datetime, None]):
        if start_date or end_date:
            return await self._filter_by_date(Income, user_id, start_date, end_date)
        return await self._all(Income, user_id)

    async def get_income_sum(self, start_date: datetime, end_date: datetime):
        return await self._amount_sum(Income, start_date, end_date)

    async def create(self, data: CreateFinance):
        income = Income(**data.dict())
        query = select(Income).filter(Income.id == income.account_id)
        result = await self.session.execute(query)
        account = self._first(result=result)
        account[0].amount += income.amount
        return await self._add(obj=Income, data=data)

    async def get_income_by_id(self, pk):
        result = await self._filter_by_id(obj=Income, pk=pk)
        return result[0]

    async def get_income_list_by_category(
            self, category_id: int, start_date: Union[datetime, None], end_date: Union[datetime, None]
    ) -> list:
        return await self._filter_by_category_id(
            obj=Income, start_date=start_date, end_date=end_date, category_id=category_id
        )


class ExpenseEntity(FinanceEntityBase):
    """ Обращение к БД расходов """
    async def get_expense_list(self, user_id: int, start_date: Union[datetime, None], end_date: Union[datetime, None]):
        if start_date or end_date:
            return await self._filter_by_date(Expense, user_id, start_date, end_date)
        return await self._all(Expense, user_id)

    async def get_expense_sum(self, start_date: datetime, end_date: datetime):
        return await self._amount_sum(Expense, start_date, end_date)

    async def create(self, data: CreateFinance):
        expense = Expense(**data.dict())
        query = select(Income).filter(Expense.id == expense.account_id)
        result = await self.session.execute(query)
        account = self._first(result=result)
        account[0].amount += expense.amount
        return await self._add(obj=Expense, data=data)

    async def get_expense_by_id(self, pk):
        result = await self._filter_by_id(obj=Expense, pk=pk)
        return result[0]

    async def get_expense_list_by_category(
            self, category_id: int, start_date: Union[datetime, None], end_date: Union[datetime, None]
    ) -> list:
        return await self._filter_by_category_id(
            obj=Expense, start_date=start_date, end_date=end_date, category_id=category_id
        )


class CurrencyEntity(Base):
    """Обращение к БД валют """
    async def get_currency_list(self):
        return await self._all(Currency)

    async def create(self, data: CreateCurrency):
        return await self._add(obj=Currency, data=data)

    async def get_currency_by_id(self, pk):
        result = await self._filter_by_id(obj=Currency, pk=pk)
        return result[0]


class CategoryEntity(Base):
    """Обращение к БД категорий """
    async def get_category_list(self):
        return await self._all(Category)

    async def det_category_count(self):
        result = await self._all(Category)
        return self._count(result)

    async def create(self, data: CreateCategory):
        return await self._add(obj=Category, data=data)

    async def get_category_by_id(self, pk):
        result = await self._filter_by_id(obj=Category, pk=pk)
        return result[0]


class AccountEntity(Base):
    """Обращение к БД счетов """
    async def get_account_list(self):
        return await self._all(Account)

    async def det_account_count(self):
        result = self._all(Account)
        return await self._count(result)

    async def create(self, data: CreateAccount):
        return await self._add(obj=Account, data=data)

    async def get_account_by_id(self, pk):
        result = await self._filter_by_id(obj=Account, pk=pk)
        return result[0]

    async def get_account_sum(self, user_id: int):
        query = select(Currency.name, func.sum(Account.amount).label("total")).\
            join(Account.currency).\
            filter(Account.add_to_balance).\
            filter(Account.user_id == user_id).\
            group_by(Currency.name)
        result = await self.session.execute(query)
        row = result.all()
        return [{data[0]: data[1]} for data in row]
