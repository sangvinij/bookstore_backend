import uuid
from typing import Any, Optional, Union

import shortuuid
from pydantic import EmailStr

from fastapi_users import schemas, models as fu_models


class UserRead(schemas.BaseUser[uuid.UUID]):
    id: fu_models.ID
    username: Union[str, shortuuid.uuid]
    email: EmailStr


class UserCreate(schemas.BaseUserCreate):
    email: EmailStr
    username: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    password: str
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False


class UserUpdate(schemas.BaseUserUpdate):
    password: Optional[str] = None
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = None
    is_superuser: Optional[bool] = None
    is_verified: Optional[bool] = None
