import uuid

from fastapi_users import FastAPIUsers

from .auth import auth_backend
from .manager import get_user_manager
from .models import User

users = FastAPIUsers[User, uuid.UUID](
    get_user_manager,
    [auth_backend],
)

current_user = users.current_user(verified=True)
superuser = users.current_user(active=True, superuser=True)
