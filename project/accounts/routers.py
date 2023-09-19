import uuid
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Body, Query
from fastapi.responses import JSONResponse
from fastapi_pagination import Page, add_pagination, Params
from fastapi_pagination.ext.sqlalchemy import paginate

from project.accounts.auth import auth_backend
from project.accounts.models import User
from project.accounts.permissions import current_user, users, superuser
from project.accounts.schemas import UserRead, UserCreate, UserUpdate, EmailVerify
from project.accounts.utils import hash_verification_code, get_verification_url, generate_verification_code, \
    send_verification_email

from sqlalchemy import update, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import NoResultFound
from sqlalchemy import asc, desc

from project.config import VERIFICATION_CODE_TTL
from project.db_settings import get_async_session


accounts_router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

accounts_router.include_router(
    users.get_auth_router(auth_backend),
    prefix="/jwt",
)

accounts_router.include_router(
    users.get_register_router(UserRead, UserCreate),
)

accounts_router.include_router(
    users.get_users_router(
        UserRead, UserUpdate,
    ),
    prefix="/users"
)


@accounts_router.get(r"/users/{user_id}/verify_email/{token}")
async def verify_user(user_id: uuid.UUID, token: str, session: AsyncSession = Depends(get_async_session)):
    verification_code = hash_verification_code(token)
    try:
        query = await session.execute(select(User).filter_by(id=user_id))
        user = query.scalar_one()
    except NoResultFound:
        raise HTTPException(status_code=400, detail="invalid user id")

    if verification_code != user.verification_code:
        return JSONResponse(status_code=404, content={"detail": "invalid link"})

    if user.is_verified:
        raise HTTPException(status_code=400, detail="user already verified")

    if user.verification_code_expiry < datetime.utcnow():
        stmt = update(User).filter_by(id=user_id).values(verification_code=None, verification_code_expiry=None)
        await session.execute(stmt)
        await session.commit()
        raise HTTPException(status_code=400, detail="verification link expired")

    stmt = update(User).filter_by(id=user_id).values(is_verified=True)
    await session.execute(stmt)
    await session.commit()
    return JSONResponse(status_code=200, content="user successfully verified")


@accounts_router.post("/verify_email")
async def verify_email(email: EmailVerify = Body(), session: AsyncSession = Depends(get_async_session)):
    try:
        query = await session.execute(select(User).filter_by(email=email.email))
        user = query.scalar_one()
    except NoResultFound:
        raise HTTPException(status_code=400, detail="User with such email not found")

    token = generate_verification_code()
    verification_code = hash_verification_code(token)
    url = get_verification_url(user.id, token)

    smtp = update(User).values(verification_code=verification_code,
                               verification_code_expiry=VERIFICATION_CODE_TTL).filter_by(id=user.id)
    await session.execute(smtp)
    await session.commit()

    await send_verification_email(user, url)

    return JSONResponse(status_code=200, content="email has been sent")


@accounts_router.get("/users", response_model=Page[UserRead])
async def get_list_of_users(
        sort_by: str = Query("email"),
        sort_order: str = Query("asc"),
        session: AsyncSession = Depends(get_async_session),
        # user: User = Depends(superuser)
):
    if sort_order == "desc":
        query = (select(User).order_by(desc(sort_by)))
    else:
        query = (select(User).order_by(sort_by))

    paginated_query = await paginate(session, query)

    return paginated_query



add_pagination(accounts_router)
