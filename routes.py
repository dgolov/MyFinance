from fastapi import APIRouter
from MyFinance import finance
from user.auth import auth_backend
from user.schemas import UserRead, UserCreate
from user.utils import fastapi_users

routes = APIRouter()

routes.include_router(finance.router, prefix="/finance")


routes.include_router(
    fastapi_users.get_auth_router(auth_backend, requires_verification=True),
    prefix="/auth/jwt",
    tags=["auth"],
)

routes.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)
