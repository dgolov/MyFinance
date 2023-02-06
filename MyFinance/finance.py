from fastapi import APIRouter, Query
from MyFinance.schemas import IncomeList, ExpenseList
from typing import Union


router = APIRouter()


@router.get("/income")
def get_income(income: str = Query(None, description="Search income"), date: Union[str] = None):
    return income


@router.get("/income/{id}")
def get_income_by_id(pk):
    return {"key": pk}


@router.post("/income", response_model=IncomeList)
def create_income(income: IncomeList):
    return income


@router.get("/expense")
def get_expense(expense: str = Query(None, description="Search expense"), date: Union[str] = None):
    return expense


@router.get("/expense/{id}")
def get_expense_by_id(pk):
    return {"key": pk}


@router.post("/expense")
def create_expense(expense: ExpenseList):
    return expense
