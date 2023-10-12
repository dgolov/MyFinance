import asyncio

from sqlalchemy.ext.asyncio import AsyncSession
from core.engine import get_async_session
from core import repository_entity
from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from MyFinance import schemas
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
        repository_entity.AccountEntity(session).get_account_sum(user_id=user.id),
        get_income_list(user, session, start_date_str, end_date_str),
        get_expense_list(user, session, start_date_str, end_date_str)
    )
    return {
        "account_sum": account_sum,
        "income": income,
        "expense_sum": expense,
    }


@router.get("/income", response_model=List[schemas.IncomeSchema])
async def get_income_list(
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session),
        start_date_str: Union[str, None] = None,
        end_date_str: Union[str, None] = None
) -> List[schemas.IncomeSchema]:
    start_date, end_date = get_formatted_datetime(start=start_date_str, end=end_date_str)
    return await repository_entity.IncomeEntity(session).get_income_list(user.id, start_date, end_date)


@router.get("/income/{id}", response_model=Union[schemas.IncomeSchema, None])
async def get_income_by_id(
        pk: int,
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
) -> Union[schemas.IncomeSchema, None]:
    return await repository_entity.IncomeEntity(session).get_income_by_id(pk, user.id)


@router.get("/income/category/{id}", response_model=List[schemas.IncomeSchema])
async def get_income_by_category_id(
        pk: int,
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session),
        start_date_str: Union[str, None] = None,
        end_date_str: Union[str, None] = None
) -> List[schemas.IncomeSchema]:
    start_date, end_date = get_formatted_datetime(start=start_date_str, end=end_date_str)
    return await repository_entity.IncomeEntity(session).get_income_list_by_category(pk, user.id, start_date, end_date)


@router.post("/income")
async def create_income(
        data: schemas.CreateFinance,
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
) -> JSONResponse:
    result = await repository_entity.IncomeEntity(session).create(data, user.id)
    return prepare_response(result, success_status_code=status.HTTP_201_CREATED)


@router.patch("/income/{id}")
async def update_income(
        pk: int,
        data: schemas.CreateFinance,
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
) -> JSONResponse:
    result = await repository_entity.IncomeEntity(session).update(pk, data, user.id)
    return prepare_response(result)


@router.delete("/income/{id}")
async def delete_income(
        pk: int,
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
) -> JSONResponse:
    result = await repository_entity.IncomeEntity(session).delete(pk, user.id)
    return prepare_response(result)


@router.get("/expense", response_model=List[schemas.ExpenseSchema])
async def get_expense_list(
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session),
        start_date_str: Union[str, None] = None,
        end_date_str: Union[str, None] = None
) -> List[schemas.ExpenseSchema]:
    start_date, end_date = get_formatted_datetime(start=start_date_str, end=end_date_str)
    return await repository_entity.ExpenseEntity(session).get_expense_list(user.id, start_date, end_date)


@router.get("/expense/{id}", response_model=Union[schemas.ExpenseSchema, None])
async def get_expense_by_id(
        pk: int, user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
) -> Union[schemas.ExpenseSchema, None]:
    return await repository_entity.ExpenseEntity(session).get_expense_by_id(pk, user.id)


@router.get("/expense/category/{id}", response_model=List[schemas.ExpenseSchema])
async def get_expense_by_category_id(
        pk: int,
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session),
        start_date_str: Union[str, None] = None,
        end_date_str: Union[str, None] = None
) -> List[schemas.ExpenseSchema]:
    start_date, end_date = get_formatted_datetime(start=start_date_str, end=end_date_str)
    return await repository_entity.ExpenseEntity(session).get_expense_list_by_category(
        pk, user.id, start_date, end_date
    )


@router.post("/expense")
async def create_expense(
        data: schemas.CreateFinance,
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
) -> JSONResponse:
    result = await repository_entity.ExpenseEntity(session).create(data, user.id)
    return prepare_response(result, success_status_code=status.HTTP_201_CREATED)


@router.patch("/expense/{id}")
async def update_expense(
        pk: int, data: schemas.CreateFinance,
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
) -> JSONResponse:
    result = await repository_entity.ExpenseEntity(session).update(pk, data, user.id)
    return prepare_response(result)


@router.delete("/expense/{id}")
async def delete_expense(
        pk: int,
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
) -> JSONResponse:
    result = await repository_entity.ExpenseEntity(session).delete(pk, user.id)
    return prepare_response(result)


@router.get("/category", response_model=List[schemas.CategorySchema])
async def get_category_list(
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
) -> List[schemas.CategorySchema]:
    return await repository_entity.CategoryEntity(session).get_category_list(user.id)


@router.get("/category/{id}", response_model=Union[schemas.CategorySchema, None])
async def get_category_by_id(
        pk: int, user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
) -> Union[schemas.CategorySchema, None]:
    return await repository_entity.CategoryEntity(session).get_category_by_id(pk, user.id)


@router.post("/category")
async def create_category(
        data: schemas.CreateCategory,
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
) -> JSONResponse:
    result = await repository_entity.CategoryEntity(session).create(user.id, data)
    return prepare_response(result, success_status_code=status.HTTP_201_CREATED)


@router.patch("/category/{id}")
async def update_category(
        pk: int,
        data: schemas.CreateCategory,
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
) -> JSONResponse:
    result = await repository_entity.CategoryEntity(session).update(pk, data, user.id)
    return prepare_response(result)


@router.delete("/category/{id}")
async def delete_category(
        pk: int,
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
) -> JSONResponse:
    result = await repository_entity.CategoryEntity(session).delete(pk, user.id)
    return prepare_response(result)


@router.get("/currency", response_model=List[schemas.CurrencySchema])
async def get_currency_list(
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
) -> List[schemas.CurrencySchema]:
    return await repository_entity.CurrencyEntity(session).get_currency_list(user.id)


@router.get("/currency/{id}", response_model=Union[schemas.CurrencySchema, None])
async def get_currency_by_id(
        pk: int,
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
) -> Union[schemas.CurrencySchema, None]:
    return await repository_entity.CurrencyEntity(session).get_currency_by_id(pk, user.id)


@router.post("/currency")
async def create_currency(
        data: schemas.CreateCurrency,
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
) -> JSONResponse:
    result = await repository_entity.CurrencyEntity(session).create(user.id, data)
    return prepare_response(result, success_status_code=status.HTTP_201_CREATED)


@router.patch("/currency/{id}")
async def update_currency(
        pk: int,
        data: schemas.CreateCurrency,
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
) -> JSONResponse:
    result = await repository_entity.CurrencyEntity(session).update(pk, data, user.id)
    return prepare_response(result)


@router.delete("/currency/{id}")
async def delete_currency(
        pk: int,
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
) -> JSONResponse:
    result = await repository_entity.CategoryEntity(session).delete(pk, user.id)
    return prepare_response(result)


@router.get("/account", response_model=List[schemas.AccountSchema])
async def get_account_list(
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
) -> List[schemas.AccountSchema]:
    return await repository_entity.AccountEntity(session).get_account_list(user.id)


@router.get("/account/{id}", response_model=Union[schemas.AccountSchema, None])
async def get_account_by_id(
        pk: int,
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
) -> Union[schemas.AccountSchema, None]:
    return await repository_entity.AccountEntity(session).get_account_by_id(pk, user.id)


@router.post("/account")
async def create_account(
        data: schemas.CreateAccount,
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
) -> JSONResponse:
    result = await repository_entity.AccountEntity(session).create(data, user.id)
    return prepare_response(result, success_status_code=status.HTTP_201_CREATED)


@router.patch("/account/{id}")
async def update_currency(
        pk: int,
        data: schemas.CreateAccount,
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
) -> JSONResponse:
    result = await repository_entity.AccountEntity(session).update(pk, data, user.id)
    return prepare_response(result)


@router.delete("/account/{id}")
async def delete_account(
        pk: int,
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
) -> JSONResponse:
    result = await repository_entity.AccountEntity(session).delete(pk, user.id)
    return prepare_response(result)
