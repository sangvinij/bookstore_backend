from fastapi import APIRouter, Depends

from project.accounts.auth import auth_backend, google_oauth_client

from project.accounts.models import User
from project.accounts.permissions import current_user, users
from project.accounts.schemas import UserRead, UserCreate
from project.env_config import env


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
    users.get_oauth_router(google_oauth_client, auth_backend, env.SECRET_KEY),
    prefix="/google",
)

accounts_router.include_router(
    users.get_oauth_associate_router(google_oauth_client, UserRead, env.SECRET_KEY),
    prefix="/associate/google",
)


@accounts_router.get(r"/users/me")
def protected_route(user: User = Depends(current_user)):
    return user
