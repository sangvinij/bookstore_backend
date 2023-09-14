import uuid
from typing import Optional

from fastapi_users import BaseUserManager, UUIDIDMixin
from fastapi import Depends, Request

from project.accounts.auth import get_user_db
from project.accounts.models import User
from project.env_config import env


class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):
    reset_password_token_secret = env.SECRET_KEY
    verification_token_secret = env.SECRET_KEY

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        print(f"User {user.id} has registered.")


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)
