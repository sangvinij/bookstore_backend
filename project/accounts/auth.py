from fastapi import Depends

from fastapi_users.authentication import BearerTransport, JWTStrategy
from fastapi_users.db import SQLAlchemyUserDatabase

from project.db_settings import get_async_session
from project.env_config import env

from sqlalchemy.ext.asyncio import AsyncSession

from .backends import CustomAuthenticationBackend
from .models import User

bearer_transport = BearerTransport(tokenUrl="auth/users/login")


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=env.SECRET_KEY, lifetime_seconds=3600)


auth_backend = CustomAuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)
