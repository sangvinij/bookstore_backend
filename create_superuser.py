import asyncio

from fastapi_users.password import PasswordHelper


from project.accounts.models import User
from project.env_config import env

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine


engine = create_async_engine(env.DATABASE_URL, echo=True)

async_session = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


async def create_superuser():
    async with async_session() as session:
        query = await session.execute(select(User).filter_by(email=env.SUPERUSER_EMAIL))
        if query.all():
            return

        password_helper = PasswordHelper()
        hashed_password = password_helper.hash(env.SUPERUSER_PASSWORD)
        user = User(email=env.SUPERUSER_EMAIL, hashed_password=hashed_password, is_superuser=True, is_verified=True)
        session.add(user)
        await session.commit()


if __name__ == "__main__":
    asyncio.run(create_superuser())
