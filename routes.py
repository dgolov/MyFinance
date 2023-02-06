from fastapi import APIRouter
from MyFinance import finance


routes = APIRouter()

routes.include_router(finance.router, prefix="/finance")
