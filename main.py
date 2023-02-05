from fastapi import FastAPI, Query
from schemas import Income, Expense


app = FastAPI()


@app.get("/income")
def get_income(income: str = Query(None, description="Search income")):
    return income


@app.post("/income")
def create_income(income: Income):
    return income


@app.get("/expense")
def get_expense(expense: str = Query(None, description="Search expense")):
    return expense


@app.post("/expense")
def create_expense(expense: Expense):
    return expense
