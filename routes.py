from fastapi import APIRouter
from fastapi_users import FastAPIUsers, fastapi_users
from MyFinance import finance
from user.models import User
from user.auth import auth_backend
from user.manager import get_user_manager


routes = APIRouter()

routes.include_router(finance.router, prefix="/finance")


fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

routes.include_router(
    fastapi_users.get_auth_router(auth_backend, requires_verification=True),
    prefix="/auth/jwt",
    tags=["auth"],
)
