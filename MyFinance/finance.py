import asyncio

from sqlalchemy.ext.asyncio import AsyncSession
from core.engine import get_async_session
from core.repository_entity import IncomeEntity, ExpenseEntity, CategoryEntity, CurrencyEntity, AccountEntity
from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from MyFinance.schemas import CreateCategory, CreateAccount, CreateCurrency, CreateFinance, AccountSchema, \
    IncomeSchema, ExpenseSchema, CurrencySchema, CategorySchema
from MyFinance.services import get_formatted_datetime, prepare_response
from typing import Union, List
from users.models import User
from users.utils import current_user


router = APIRouter()


@router.get("/")
async def main(
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session),
        start_date_str: Union[str, None] = None,
        end_date_str: Union[str, None] = None
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
        start_date_str: Union[str, None] = None,
        end_date_str: Union[str, None] = None
) -> List[IncomeSchema]:
    start_date, end_date = get_formatted_datetime(start=start_date_str, end=end_date_str)
    return await IncomeEntity(session).get_income_list(user.id, start_date, end_date)


@router.get("/income/{id}", response_model=Union[IncomeSchema, None])
async def get_income_by_id(
        pk: int, user: User = Depends(current_user), session: AsyncSession = Depends(get_async_session)
) -> Union[IncomeSchema, None]:
    return await IncomeEntity(session).get_income_by_id(pk, user.id)


@router.get("/income/category/{id}", response_model=List[IncomeSchema])
async def get_income_by_category_id(
        pk: int,
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session),
        start_date_str: Union[str, None] = None,
        end_date_str: Union[str, None] = None
) -> List[IncomeSchema]:
    start_date, end_date = get_formatted_datetime(start=start_date_str, end=end_date_str)
    return await IncomeEntity(session).get_income_list_by_category(pk, user.id, start_date, end_date)


@router.post("/income")
async def create_income(
        data: CreateFinance,
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
) -> JSONResponse:
    result = await IncomeEntity(session).create(data, user.id)
    return prepare_response(result, success_status_code=status.HTTP_201_CREATED)


@router.patch("/income/{id}")
async def update_income(
        pk: int,
        data: CreateFinance,
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
) -> JSONResponse:
    result = await IncomeEntity(session).update(pk, data, user.id)
    return prepare_response(result)


@router.delete("/income/{id}")
async def delete_income(
        pk: int,
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
) -> JSONResponse:
    result = await IncomeEntity(session).delete(pk, user.id)
    return prepare_response(result)


@router.get("/expense", response_model=List[ExpenseSchema])
async def get_expense_list(
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session),
        start_date_str: Union[str, None] = None,
        end_date_str: Union[str, None] = None
) -> List[ExpenseSchema]:
    start_date, end_date = get_formatted_datetime(start=start_date_str, end=end_date_str)
    return await ExpenseEntity(session).get_expense_list(user.id, start_date, end_date)


@router.get("/expense/{id}", response_model=Union[ExpenseSchema, None])
async def get_expense_by_id(
        pk: int, user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
) -> Union[ExpenseSchema, None]:
    return await ExpenseEntity(session).get_expense_by_id(pk, user.id)


@router.get("/expense/category/{id}", response_model=List[ExpenseSchema])
async def get_expense_by_category_id(
        pk: int,
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session),
        start_date_str: Union[str, None] = None,
        end_date_str: Union[str, None] = None
) -> List[ExpenseSchema]:
    start_date, end_date = get_formatted_datetime(start=start_date_str, end=end_date_str)
    return await ExpenseEntity(session).get_expense_list_by_category(pk, user.id, start_date, end_date)


@router.post("/expense")
async def create_expense(
        data: CreateFinance,
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
) -> JSONResponse:
    result = await ExpenseEntity(session).create(data, user.id)
    return prepare_response(result, success_status_code=status.HTTP_201_CREATED)


@router.patch("/expense/{id}")
async def update_expense(
        pk: int, data: CreateFinance,
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
) -> JSONResponse:
    result = await ExpenseEntity(session).update(pk, data, user.id)
    return prepare_response(result)


@router.delete("/expense/{id}")
async def delete_expense(
        pk: int,
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
) -> JSONResponse:
    result = await ExpenseEntity(session).delete(pk, user.id)
    return prepare_response(result)


@router.get("/category", response_model=List[CategorySchema])
async def get_category_list(
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
) -> List[CategorySchema]:
    return await CategoryEntity(session).get_category_list(user.id)


@router.get("/category/{id}", response_model=Union[CategorySchema, None])
async def get_category_by_id(
        pk: int, user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
) -> Union[CategorySchema, None]:
    return await CategoryEntity(session).get_category_by_id(pk, user.id)


@router.post("/category")
async def create_category(
        data: CreateCategory,
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
) -> JSONResponse:
    result = await CategoryEntity(session).create(user.id, data)
    return prepare_response(result, success_status_code=status.HTTP_201_CREATED)


@router.patch("/category/{id}")
async def update_category(
        pk: int,
        data: CreateCategory,
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
) -> JSONResponse:
    result = await CategoryEntity(session).update(pk, data, user.id)
    return prepare_response(result)


@router.delete("/category/{id}")
async def delete_category(
        pk: int,
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
) -> JSONResponse:
    result = await CategoryEntity(session).delete(pk, user.id)
    return prepare_response(result)


@router.get("/currency", response_model=List[CurrencySchema])
async def get_currency_list(
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
) -> List[CurrencySchema]:
    return await CurrencyEntity(session).get_currency_list(user.id)


@router.get("/currency/{id}", response_model=Union[CurrencySchema, None])
async def get_currency_by_id(
        pk: int,
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
) -> Union[CurrencySchema, None]:
    return await CurrencyEntity(session).get_currency_by_id(pk, user.id)


@router.post("/currency")
async def create_currency(
        data: CreateCurrency,
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
) -> JSONResponse:
    result = await CurrencyEntity(session).create(user.id, data)
    return prepare_response(result, success_status_code=status.HTTP_201_CREATED)


@router.patch("/currency/{id}")
async def update_currency(
        pk: int,
        data: CreateCurrency,
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
) -> JSONResponse:
    result = await CurrencyEntity(session).update(pk, data, user.id)
    return prepare_response(result)


@router.delete("/currency/{id}")
async def delete_currency(
        pk: int,
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
) -> JSONResponse:
    result = await CategoryEntity(session).delete(pk, user.id)
    return prepare_response(result)


@router.get("/account", response_model=List[AccountSchema])
async def get_account_list(
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
) -> List[AccountSchema]:
    return await AccountEntity(session).get_account_list(user.id)


@router.get("/account/{id}", response_model=Union[AccountSchema, None])
async def get_account_by_id(
        pk: int, user: User = Depends(current_user), session: AsyncSession = Depends(get_async_session)
) -> Union[AccountSchema, None]:
    return await AccountEntity(session).get_account_by_id(pk, user.id)


@router.post("/account")
async def create_account(
        data: CreateAccount,
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
) -> JSONResponse:
    result = await AccountEntity(session).create(data, user.id)
    return prepare_response(result, success_status_code=status.HTTP_201_CREATED)


@router.patch("/account/{id}")
async def update_currency(
        pk: int,
        data: CreateAccount,
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
) -> JSONResponse:
    result = await AccountEntity(session).update(pk, data, user.id)
    return prepare_response(result)


@router.delete("/account/{id}")
async def delete_account(
        pk: int,
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
) -> JSONResponse:
    result = await AccountEntity(session).delete(pk, user.id)
    return prepare_response(result)
