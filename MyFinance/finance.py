import asyncio

from sqlalchemy.ext.asyncio import AsyncSession
from core.engine import get_async_session
from core.repository_entity import IncomeEntity, ExpenseEntity, CategoryEntity, CurrencyEntity, AccountEntity
from fastapi import APIRouter, Depends
from MyFinance.schemas import CreateCategory, CreateAccount, CreateCurrency, CreateFinance, AccountSchema, \
    IncomeSchema, ExpenseSchema, CurrencySchema, CategorySchema
from MyFinance.services import get_formatted_datetime
from typing import Union, List


router = APIRouter()


@router.get("/")
async def main(
        session: AsyncSession = Depends(get_async_session),
        start_date_str: Union[str, None] = None, end_date_str: Union[str, None] = None
) -> dict:
    account_sum, income, expense = await asyncio.gather(
        AccountEntity(session).get_account_sum(),
        get_income_list(session, start_date_str, end_date_str),
        get_expense_list(session, start_date_str, end_date_str)
    )
    return {
        "account_sum": account_sum,
        "income": income,
        "expense_sum": expense,
    }


@router.get("/income", response_model=List[IncomeSchema])
async def get_income_list(
        session: AsyncSession = Depends(get_async_session),
        start_date_str: Union[str, None] = None, end_date_str: Union[str, None] = None
) -> list:
    start_date, end_date = get_formatted_datetime(start=start_date_str, end=end_date_str)
    response = await IncomeEntity(session).get_income_list(start_date, end_date)
    return response


@router.get("/income/{id}", response_model=IncomeSchema)
async def get_income_by_id(pk, session: AsyncSession = Depends(get_async_session)):
    return await IncomeEntity(session).get_income_by_id(pk)


@router.get("/income/category/{id}", response_model=List[IncomeSchema])
def get_income_by_category_id(
        pk, session: AsyncSession = Depends(get_async_session),
        start_date_str: Union[str, None] = None, end_date_str: Union[str, None] = None
):
    start_date, end_date = get_formatted_datetime(start=start_date_str, end=end_date_str)
    return IncomeEntity(session).get_income_list_by_category(pk, start_date, end_date)


@router.post("/income")
def create_income(data: CreateFinance, session: AsyncSession = Depends(get_async_session)):
    return IncomeEntity(session).create(data)


@router.get("/expense", response_model=List[ExpenseSchema])
async def get_expense_list(session: AsyncSession = Depends(get_async_session), start_date_str: Union[str, None] = None, end_date_str: Union[str, None] = None) -> dict:
    start_date, end_date = get_formatted_datetime(start=start_date_str, end=end_date_str)
    return await ExpenseEntity(session).get_expense_list(start_date, end_date)


@router.get("/expense/{id}", response_model=ExpenseSchema)
def get_expense_by_id(pk, session: AsyncSession = Depends(get_async_session)):
    return ExpenseEntity(session).get_expense_by_id(pk)


@router.get("/expense/category/{id}", response_model=List[ExpenseSchema])
def get_expense_by_category_id(
        pk, session: AsyncSession = Depends(get_async_session),
        start_date_str: Union[str, None] = None, end_date_str: Union[str, None] = None
):
    start_date, end_date = get_formatted_datetime(start=start_date_str, end=end_date_str)
    return ExpenseEntity(session).get_expense_list_by_category(pk, start_date, end_date)


@router.post("/expense")
def create_expense(data: CreateFinance, session: AsyncSession = Depends(get_async_session)):
    return ExpenseEntity(session).create(data)


@router.get("/category", response_model=List[CategorySchema])
def get_category_list(session: AsyncSession = Depends(get_async_session)):
    income = CategoryEntity(session).get_category_list()
    return income


@router.get("/category/{id}", response_model=CategorySchema)
def get_category_by_id(pk: int, session: AsyncSession = Depends(get_async_session)):
    return CategoryEntity(session).get_category_by_id(pk)


@router.post("/category")
def create_category(data: CreateCategory, session: AsyncSession = Depends(get_async_session)):
    return CategoryEntity(session).create(data)


@router.get("/currency", response_model=List[CurrencySchema])
def get_currency_list(session: AsyncSession = Depends(get_async_session)):
    income = CurrencyEntity(session).get_currency_list()
    return income


@router.get("/currency/{id}", response_model=CurrencySchema)
def get_currency_by_id(pk: int, session: AsyncSession = Depends(get_async_session)):
    return CurrencyEntity(session).get_currency_by_id(pk)


@router.post("/currency")
def create_currency(data: CreateCurrency, session: AsyncSession = Depends(get_async_session)):
    return CurrencyEntity(session).create(data)


@router.get("/account", response_model=List[AccountSchema])
def get_account_list(session: AsyncSession = Depends(get_async_session)):
    income = AccountEntity(session).get_account_list()
    return income


@router.get("/account/{id}", response_model=AccountSchema)
def get_account_by_id(pk: int, session: AsyncSession = Depends(get_async_session)):
    return AccountEntity(session).get_account_by_id(pk)


@router.post("/account")
def create_account(data: CreateAccount, session: AsyncSession = Depends(get_async_session)):
    return AccountEntity(session).create(data)
