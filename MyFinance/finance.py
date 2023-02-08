from core.repository_entity import IncomeEntity, ExpenseEntity, CategoryEntity, CurrencyEntity, AccountEntity
from core.utils import get_db
from fastapi import APIRouter, Depends
from MyFinance.schemas import CreateCategory, CreateAccount, CreateCurrency, CreateFinance
from MyFinance.services import get_formatted_datetime, create_formatted_datetime
from sqlalchemy.orm import Session
from typing import Union


router = APIRouter()


@router.get("/")
def main(
        db: Session = Depends(get_db), start_date_str: Union[str, None] = None, end_date_str: Union[str, None] = None
) -> dict:
    start_date, end_date = create_formatted_datetime(start=start_date_str, end=end_date_str)
    return {
        "account_sum": AccountEntity(db).get_account_sum(),
        "income_sum": IncomeEntity(db).get_income_sum(start_date, end_date),
        "expense_sum": ExpenseEntity(db).get_expense_sum(start_date, end_date),
    }


@router.get("/income")
def get_income_list(
        db: Session = Depends(get_db), start_date_str: Union[str, None] = None, end_date_str: Union[str, None] = None
) -> list:
    start_date, end_date = get_formatted_datetime(start=start_date_str, end=end_date_str)
    return IncomeEntity(db).get_income_list(start_date, end_date)


@router.get("/income/{id}")
def get_income_by_id(pk, db: Session = Depends(get_db)):
    return IncomeEntity(db).get_income_by_id(pk)


@router.get("/income/category/{id}")
def get_income_by_category_id(
        pk, db: Session = Depends(get_db),
        start_date_str: Union[str, None] = None, end_date_str: Union[str, None] = None
):
    start_date, end_date = get_formatted_datetime(start=start_date_str, end=end_date_str)
    return IncomeEntity(db).get_income_list_by_category(pk, start_date, end_date)


@router.post("/income")
def create_income(data: CreateFinance, db: Session = Depends(get_db)):
    return IncomeEntity(db).create(data)


@router.get("/expense")
def get_expense(db: Session = Depends(
    get_db), start_date_str: Union[str, None] = None, end_date_str: Union[str, None] = None
) -> dict:
    start_date, end_date = get_formatted_datetime(start=start_date_str, end=end_date_str)
    return ExpenseEntity(db).get_expense_list(start_date, end_date)


@router.get("/expense/{id}")
def get_expense_by_id(pk, db: Session = Depends(get_db)):
    return ExpenseEntity(db).get_expense_by_id(pk)


@router.get("/expense/category/{id}")
def get_expense_by_category_id(
        pk, db: Session = Depends(get_db),
        start_date_str: Union[str, None] = None, end_date_str: Union[str, None] = None
):
    start_date, end_date = get_formatted_datetime(start=start_date_str, end=end_date_str)
    return ExpenseEntity(db).get_expense_list_by_category(pk, start_date, end_date)


@router.post("/expense")
def create_expense(data: CreateFinance, db: Session = Depends(get_db)):
    return ExpenseEntity(db).create(data)


@router.get("/category")
def get_category_list(db: Session = Depends(get_db)):
    income = CategoryEntity(db).get_category_list()
    return income


@router.get("/category/{id}")
def get_category_by_id(pk: int, db: Session = Depends(get_db)):
    return CategoryEntity(db).get_category_by_id(pk)


@router.post("/category")
def create_category(data: CreateCategory, db: Session = Depends(get_db)):
    return CategoryEntity(db).create(data)


@router.get("/currency")
def get_currency_list(db: Session = Depends(get_db)):
    income = CurrencyEntity(db).get_currency_list()
    return income


@router.get("/currency/{id}")
def get_currency_by_id(pk: int, db: Session = Depends(get_db)):
    return CurrencyEntity(db).get_currency_by_id(pk)


@router.post("/currency")
def create_currency(data: CreateCurrency, db: Session = Depends(get_db)):
    return CurrencyEntity(db).create(data)


@router.get("/account")
def get_account_list(db: Session = Depends(get_db)):
    income = AccountEntity(db).get_account_list()
    return income


@router.get("/account/{id}")
def get_account_by_id(pk: int, db: Session = Depends(get_db)):
    return AccountEntity(db).get_account_by_id(pk)


@router.post("/account")
def create_account(data: CreateAccount, db: Session = Depends(get_db)):
    return AccountEntity(db).create(data)
