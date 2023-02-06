from core.repository_entity import IncomeEntity, ExpenseEntity, CategoryEntity, CurrencyEntity, AccountEntity
from core.utils import get_db
from fastapi import APIRouter, Depends
from MyFinance.schemas import CreateCategory, CreateAccount, CreateCurrency, CreateFinance, IncomeList, ExpenseList, \
    CurrencyList, CategoryList, AccountList
from sqlalchemy.orm import Session
from typing import Union


router = APIRouter()


@router.get("/income")
def get_income_list(db: Session = Depends(get_db), date: Union[str] = None):
    return IncomeEntity(db).get_income_list(date)


@router.get("/income/{id}")
def get_income_by_id(pk, db: Session = Depends(get_db)):
    return IncomeEntity(db).get_income_by_id(pk)


@router.post("/income")
def create_income(data: CreateFinance, db: Session = Depends(get_db)):
    return IncomeEntity(db).create(data)


@router.get("/expense")
def get_expense(db: Session = Depends(get_db), date: Union[str] = None):
    return ExpenseEntity(db).get_expense_list(date)


@router.get("/expense/{id}")
def get_expense_by_id(pk, db: Session = Depends(get_db)):
    return ExpenseEntity(db).get_expense_by_id(pk)


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
