import asyncio

from sqlalchemy.ext.asyncio import AsyncSession
from core.engine import get_async_session
from core.repository_entity import IncomeEntity, ExpenseEntity, CategoryEntity, CurrencyEntity, AccountEntity
from fastapi import APIRouter, Depends
from MyFinance.schemas import CreateCategory, CreateAccount, CreateCurrency, CreateFinance, AccountSchema, \
    IncomeSchema, ExpenseSchema, CurrencySchema, CategorySchema
from MyFinance.services import get_formatted_datetime
from typing import Union, List
from users.models import User
from users.utils import current_user


router = APIRouter()


@router.get("/")
async def main(
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session),
        start_date_str: Union[str, None] = None, end_date_str: Union[str, None] = None
) -> dict:
    account_sum, income, expense = await asyncio.gather(
        AccountEntity(session).get_account_sum(user_id=user.id),
        get_income_list(user, session, start_date_str, end_date_str),
        get_expense_list(user, session, start_date_str, end_date_str)
    )
    return {
        "account_sum": account_sum,
        "income": income,
        "expense_sum": expense,
    }


@router.get("/income", response_model=List[IncomeSchema])
async def get_income_list(
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session),
        start_date_str: Union[str, None] = None, end_date_str: Union[str, None] = None
) -> list:
    start_date, end_date = get_formatted_datetime(start=start_date_str, end=end_date_str)
    return await IncomeEntity(session).get_income_list(user.id, start_date, end_date)


@router.get("/income/{id}", response_model=Union[IncomeSchema, None])
async def get_income_by_id(
        pk: int, user: User = Depends(current_user), session: AsyncSession = Depends(get_async_session)
):
    return await IncomeEntity(session).get_income_by_id(pk, user.id)


@router.get("/income/category/{id}", response_model=List[IncomeSchema])
async def get_income_by_category_id(
        pk: int, user: User = Depends(current_user), session: AsyncSession = Depends(get_async_session),
        start_date_str: Union[str, None] = None, end_date_str: Union[str, None] = None
) -> list:
    start_date, end_date = get_formatted_datetime(start=start_date_str, end=end_date_str)
    return await IncomeEntity(session).get_income_list_by_category(pk, user.id, start_date, end_date)


@router.post("/income")
async def create_income(
        data: CreateFinance, user: User = Depends(current_user), session: AsyncSession = Depends(get_async_session)
):
    return await IncomeEntity(session).create(data, user.id)


@router.patch("/income/{id}")
async def update_income(
        pk: int, data: CreateFinance, user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
):
    return await IncomeEntity(session).update(pk, data, user.id)


@router.delete("/income/{id}")
async def delete_income(
        pk: int, user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
):
    return await IncomeEntity(session).delete(pk, user.id)


@router.get("/expense", response_model=List[ExpenseSchema])
async def get_expense_list(
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session),
        start_date_str: Union[str, None] = None, end_date_str: Union[str, None] = None
) -> dict:
    start_date, end_date = get_formatted_datetime(start=start_date_str, end=end_date_str)
    return await ExpenseEntity(session).get_expense_list(user.id, start_date, end_date)


@router.get("/expense/{id}", response_model=Union[ExpenseSchema, None])
async def get_expense_by_id(
        pk: int, user: User = Depends(current_user), session: AsyncSession = Depends(get_async_session)
):
    return await ExpenseEntity(session).get_expense_by_id(pk, user.id)


@router.get("/expense/category/{id}", response_model=List[ExpenseSchema])
async def get_expense_by_category_id(
        pk: int, user: User = Depends(current_user), session: AsyncSession = Depends(get_async_session),
        start_date_str: Union[str, None] = None, end_date_str: Union[str, None] = None
):
    start_date, end_date = get_formatted_datetime(start=start_date_str, end=end_date_str)
    return await ExpenseEntity(session).get_expense_list_by_category(pk, user.id, start_date, end_date)


@router.post("/expense")
async def create_expense(
        data: CreateFinance, user: User = Depends(current_user), session: AsyncSession = Depends(get_async_session)
):
    return await ExpenseEntity(session).create(data, user.id)


@router.patch("/expense/{id}")
async def update_expense(
        pk: int, data: CreateFinance, user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
):
    return await ExpenseEntity(session).update(pk, data, user.id)


@router.delete("/expense/{id}")
async def delete_expense(
        pk: int, user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
):
    return await ExpenseEntity(session).delete(pk, user.id)


@router.get("/category", response_model=List[CategorySchema])
async def get_category_list(
        user: User = Depends(current_user), session: AsyncSession = Depends(get_async_session)
) -> list:
    return await CategoryEntity(session).get_category_list(user.id)


@router.get("/category/{id}", response_model=Union[CategorySchema, None])
async def get_category_by_id(
        pk: int, user: User = Depends(current_user), session: AsyncSession = Depends(get_async_session)
):
    return await CategoryEntity(session).get_category_by_id(pk, user.id)


@router.post("/category")
async def create_category(
        data: CreateCategory, user: User = Depends(current_user), session: AsyncSession = Depends(get_async_session)
):
    return await CategoryEntity(session).create(user.id, data)


@router.patch("/category/{id}")
async def update_category(
        pk: int, data: CreateCategory, user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
):
    return await CategoryEntity(session).update(pk, data, user.id)


@router.delete("/category/{id}")
async def delete_category(
        pk: int, user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
):
    return await CategoryEntity(session).delete(pk, user.id)


@router.get("/currency", response_model=List[CurrencySchema])
async def get_currency_list(user: User = Depends(current_user), session: AsyncSession = Depends(get_async_session)):
    return await CurrencyEntity(session).get_currency_list(user.id)


@router.get("/currency/{id}", response_model=Union[CurrencySchema, None])
async def get_currency_by_id(
        pk: int, user: User = Depends(current_user), session: AsyncSession = Depends(get_async_session)
):
    return await CurrencyEntity(session).get_currency_by_id(pk, user.id)


@router.post("/currency")
async def create_currency(
        data: CreateCurrency, user: User = Depends(current_user), session: AsyncSession = Depends(get_async_session)
):
    return await CurrencyEntity(session).create(user.id, data)


@router.patch("/currency/{id}")
async def update_currency(
        pk: int, data: CreateCurrency, user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
):
    return await CurrencyEntity(session).update(pk, data, user.id)


@router.delete("/currency/{id}")
async def delete_currency(
        pk: int, user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
):
    return await CategoryEntity(session).delete(pk, user.id)


@router.get("/account", response_model=List[AccountSchema])
async def get_account_list(
        user: User = Depends(current_user), session: AsyncSession = Depends(get_async_session)
) -> list:
    return await AccountEntity(session).get_account_list(user.id)


@router.get("/account/{id}", response_model=Union[AccountSchema, None])
async def get_account_by_id(
        pk: int, user: User = Depends(current_user), session: AsyncSession = Depends(get_async_session)
):
    return await AccountEntity(session).get_account_by_id(pk, user.id)


@router.post("/account")
async def create_account(
        data: CreateAccount, user: User = Depends(current_user), session: AsyncSession = Depends(get_async_session)
):
    return await AccountEntity(session).create(data, user.id)


@router.patch("/account/{id}")
async def update_currency(
        pk: int, data: CreateAccount, user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
):
    return await AccountEntity(session).update(pk, data, user.id)


@router.delete("/account/{id}")
async def delete_account(
        pk: int, user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
):
    return await AccountEntity(session).delete(pk, user.id)
