from fastapi_users.authentication import CookieTransport, JWTStrategy

from project.accounts.backends import CustomAuthenticationBackend
from project.accounts.models import User
from project.env_config import env

from project.db_settings import get_async_session
from fastapi_users.db import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

cookie_transport = CookieTransport(cookie_name="bond", cookie_max_age=3600)


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=env.SECRET_KEY, lifetime_seconds=3600)


auth_backend = CustomAuthenticationBackend(
    name="jwt",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)
