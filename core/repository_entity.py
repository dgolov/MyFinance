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

    @staticmethod
    async def _all(result):
        row = result.all()
        return [data[0] for data in row]

    @staticmethod
    def _first(result):
        result = result.first()
        if result:
            return result[0]
        else:
            return None

    @staticmethod
    def _one(result):
        return result.one()

    @staticmethod
    def _count(result):
        return len(result)

    async def _add(self, obj, user_id, data):
        data = data.dict()
        data["user_id"] = user_id
        query = insert(obj).values(**data)
        await self.session.execute(query)
        await self.session.commit()
        return {
            "status": "success"
        }

    async def _update(self, obj, data):
        for field, value in data.dict().items():
            setattr(obj, field, value)
        await self.session.commit()
        return {
            "status": "success"
        }


class FinanceEntityBase(Base):
    """ Базобый класс обращения к БД для доходов / расходов
    """
    async def _filter_by_date(
            self, obj, user_id: int, start_date: Union[datetime, None], end_date: Union[datetime, None],
            category_id: Union[int, None] = None
    ):
        """ Фильтр доходов / расходов по датам
        :param obj: Модель расхода / дохода
        :param start_date: Начальная дата
        :param end_date: Конечныя дата
        :return: Ответ БД
        """
        return await self.__get_query_with_filter_by_date(obj, user_id, start_date, end_date, category_id)

    async def _filter_by_category_id(
            self, obj, start_date: Union[datetime, None], end_date: Union[datetime, None], user_id: int,
            category_id: int
    ) -> list:
        """ Фильтр доходов / расходов по датам
        :param obj: Модель расхода / дохода
        :param category_id: Id категории
        :return: Ответ БД
        """
        if start_date or end_date:
            return await self._filter_by_date(obj, user_id, start_date, end_date, category_id)
        query = select(Income).filter(obj.user_id == user_id).filter(obj.category_id == category_id)
        query_result = await self.session.execute(query)
        return await self._all(query_result)

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
            self, obj, user_id: int, start_date: Union[datetime, None], end_date: Union[datetime, None],
            category_id: Union[int, None]
    ):
        """ Добавление фильтра по датам в запрос
        :param obj: Модель расхода / дохода
        :param user_id: Текущий пользователь
        :param start_date: Начальная дата
        :param end_date: Конечныя дата
        :return: SQL запрос
        """
        query = select(obj).filter(obj.user_id == user_id)
        if category_id:
            query = query.filter(obj.category_id == category_id)
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
        query = select(Income).filter(Income.user_id == user_id)
        query_result = await self.session.execute(query)
        return await self._all(query_result)

    async def get_income_sum(self, start_date: datetime, end_date: datetime):
        return await self._amount_sum(Income, start_date, end_date)

    async def create(self, data: CreateFinance, user_id: int):
        income = Income(**data.dict())
        query = select(Account).filter(Account.id == income.account_id).filter(Account.user_id == user_id)
        result = await self.session.execute(query)
        account = self._first(result=result)
        if not account:
            return {
                "status": "fail",
                "message": "Account is not found"
            }
        account.amount += income.amount
        return await self._add(obj=Income, user_id=user_id, data=data)

    async def update(self, pk: int, data: CreateFinance, user_id: int):
        income = await self.session.get(Income, pk)
        if not income or income.user_id != user_id:
            return {
                "status": "fail",
                "message": "Income is not found"
            }
        return await self._update(income, data)

    async def get_income_by_id(self, pk: int, user_id: int):
        query = select(Income).filter(Income.user_id == user_id).filter(Income.id == int(pk))
        result = await self.session.execute(query)
        return self._first(result)

    async def get_income_list_by_category(
            self, category_id: int, user_id: int, start_date: Union[datetime, None], end_date: Union[datetime, None]
    ) -> list:
        return await self._filter_by_category_id(
            obj=Income, start_date=start_date, end_date=end_date, user_id=user_id, category_id=category_id
        )


class ExpenseEntity(FinanceEntityBase):
    """ Обращение к БД расходов """
    async def get_expense_list(self, user_id: int, start_date: Union[datetime, None], end_date: Union[datetime, None]):
        if start_date or end_date:
            return await self._filter_by_date(Expense, user_id, start_date, end_date)
        query = select(Expense).filter(Expense.user_id == user_id)
        query_result = await self.session.execute(query)
        return await self._all(query_result)

    async def get_expense_sum(self, start_date: datetime, end_date: datetime):
        return await self._amount_sum(Expense, start_date, end_date)

    async def create(self, data: CreateFinance, user_id: int):
        expense = Expense(**data.dict())
        query = select(Account).filter(Account.id == expense.account_id).filter(Account.user_id == user_id)
        result = await self.session.execute(query)
        account = self._first(result=result)
        if not account:
            return {
                "status": "fail",
                "message": "Account is not found"
            }
        account.amount += expense.amount
        return await self._add(obj=Expense, user_id=user_id, data=data)

    async def update(self, pk: int, data: CreateFinance, user_id: int):
        expense = await self.session.get(Expense, pk)
        if not expense or expense.user_id != user_id:
            return {
                "status": "fail",
                "message": "Income is not found"
            }
        return self._update(expense, data)

    async def get_expense_by_id(self, pk: int, user_id: int):
        query = select(Expense).filter(Income.user_id == user_id).filter(Expense.id == int(pk))
        result = await self.session.execute(query)
        return self._first(result)

    async def get_expense_list_by_category(
            self, category_id: int, user_id: int, start_date: Union[datetime, None], end_date: Union[datetime, None]
    ) -> list:
        return await self._filter_by_category_id(
            obj=Expense, start_date=start_date, end_date=end_date, user_id=user_id, category_id=category_id
        )


class CurrencyEntity(Base):
    """Обращение к БД валют """
    async def get_currency_list(self, user_id: int):
        query = select(Currency).filter(Currency.user_id == user_id or Currency.user_id == None)
        query_result = await self.session.execute(query)
        return await self._all(query_result)

    async def create(self, user_id: int, data: CreateCurrency):
        return await self._add(obj=Currency, user_id=user_id, data=data)

    async def update(self, pk: int, data: CreateCurrency, user_id: int):
        currency = await self.session.get(Currency, pk)
        if not currency or currency.user_id != user_id:
            return {
                "status": "fail",
                "message": "Currency is not found"
            }
        return await self._update(currency, data)

    async def get_currency_by_id(self, pk: int, user_id: int):
        query = select(Currency).filter(Currency.user_id == user_id).filter(Currency.id == int(pk))
        result = await self.session.execute(query)
        return self._first(result)


class CategoryEntity(Base):
    """Обращение к БД категорий """
    async def get_category_list(self, user_id: int):
        query = select(Category).filter(Category.user_id == user_id or Currency.user_id == None)
        query_result = await self.session.execute(query)
        return await self._all(query_result)

    async def det_category_count(self, user_id: int):
        query = select(Category).filter(Category.user_id == user_id or Currency.user_id == None)
        query_result = await self.session.execute(query)
        result = await self._all(query_result)
        return self._count(result)

    async def create(self, user_id: int, data: CreateCategory):
        return await self._add(obj=Category, user_id=user_id, data=data)

    async def update(self, pk: int, data: CreateCategory, user_id: int):
        category = await self.session.get(Category, pk)
        if not category or category.user_id != user_id:
            return {
                "status": "fail",
                "message": "Category is not found"
            }
        return await self._update(category, data)

    async def get_category_by_id(self, pk: int, user_id: int):
        query = select(Category).\
            filter(Category.user_id == user_id or Currency.user_id == None).\
            filter(Category.id == int(pk))
        result = await self.session.execute(query)
        return self._first(result)


class AccountEntity(Base):
    """Обращение к БД счетов """
    async def get_account_list(self, user_id: int):
        query = select(Account).filter(Account.user_id == user_id)
        query_result = await self.session.execute(query)
        return await self._all(query_result)

    async def det_account_count(self, user_id: int):
        query = select(Account).filter(Account.user_id == user_id)
        query_result = await self.session.execute(query)
        result = self._all(query_result)
        return await self._count(result)

    async def create(self, data: CreateAccount, user_id: int):
        return await self._add(obj=Account, user_id=user_id, data=data)

    async def update(self, pk: int, data: CreateAccount, user_id: int):
        account = await self.session.get(Account, pk)
        print(account)
        if not account or account.user_id != user_id:
            return {
                "status": "fail",
                "message": "Category is not found"
            }
        return await self._update(account, data)

    async def get_account_by_id(self, pk: int, user_id: int):
        query = select(Account).filter(Account.user_id == user_id).filter(Account.id == int(pk))
        result = await self.session.execute(query)
        return self._first(result)

    async def get_account_sum(self, user_id: int):
        query = select(Currency.name, func.sum(Account.amount).label("total")).\
            join(Account.currency).\
            filter(Account.add_to_balance).\
            filter(Account.user_id == user_id).\
            group_by(Currency.name)
        result = await self.session.execute(query)
        row = result.all()
        return [{data[0]: data[1]} for data in row]
