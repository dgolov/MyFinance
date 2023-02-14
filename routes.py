from fastapi import APIRouter
from MyFinance import finance
from users.auth import auth_backend
from users.schemas import UserRead, UserCreate
from users.utils import fastapi_users

routes = APIRouter()

routes.include_router(
    finance.router,
    prefix="/finance",
    tags=["finance"]
)


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

routes.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix="/auth",
    tags=["auth"],
)

routes.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["auth"],
)
