from fastapi import FastAPI, Query
from MyFinance.schemas import Income, Expense
from typing import Union


app = FastAPI()


@app.get("/income")
def get_income(income: str = Query(None, description="Search income"), date: Union[str] = None):
    return income


@app.get("/income/{id}")
def get_income_by_id(pk):
    return {"key": pk}


@app.post("/income", response_model=Income)
def create_income(income: Income):
    return income


@app.get("/expense")
def get_expense(expense: str = Query(None, description="Search expense"), date: Union[str] = None):
    return expense


@app.get("/expense/{id}")
def get_expense_by_id(pk):
    return {"key": pk}


@app.post("/expense")
def create_expense(expense: Expense):
    return expense
