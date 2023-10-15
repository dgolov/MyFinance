from config import SECRET, MAIL_USERNAME, MAIL_PASSWORD, MAIL_SERVER, MAIL_EMAIL, MAIL_PORT, logger
from typing import Optional
from fastapi import Depends, Request
from fastapi_mail import FastMail, MessageType, MessageSchema, ConnectionConfig
from fastapi_users import BaseUserManager, IntegerIDMixin
from .models import User, get_user_db


# conf = ConnectionConfig(
#     MAIL_USERNAME=MAIL_USERNAME,
#     MAIL_PASSWORD=MAIL_PASSWORD,
#     MAIL_FROM=MAIL_EMAIL,
#     MAIL_PORT=MAIL_PORT,
#     MAIL_SERVER=MAIL_SERVER,
#     MAIL_FROM_NAME="Finance app",
#     MAIL_STARTTLS=True,
#     MAIL_SSL_TLS=False,
#     USE_CREDENTIALS=True,
#     VALIDATE_CERTS=True,
# )


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    reset_password_token_secret = SECRET
    verification_token_secret = SECRET

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        # TODO Fixed send mail
        html = "example"
        message = MessageSchema(
            subject="mail example",
            recipients=user.email,
            body=html,
            subtype=MessageType.html
        )
        try:
            pass
            # fm = FastMail(conf)
            # await fm.send_message(message)
        except Exception as err:
            print(f"Error send message - {err}")
        else:
            print(f"Message has been sent to user {user.id}")
        finally:
            print(f"User {user.id} has registered.")

    async def on_after_forgot_password(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        # TODO Fixed send mail on_after_forgot_password
        print(f"User {user.id} has forgot their password. Reset token: {token}")

    async def on_after_request_verify(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        # TODO Fixed send mail on_after_request_verify WHAT IS FUCK?
        print(f"Verification requested for user {user.id}. Verification token: {token}")


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)
