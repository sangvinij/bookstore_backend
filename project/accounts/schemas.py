import uuid
from typing import Any, Optional, Union

import shortuuid
from pydantic import EmailStr, BaseModel

from fastapi_users import schemas, models as fu_models


class UserRead(schemas.BaseUser[uuid.UUID]):
    id: fu_models.ID
    email: EmailStr
    first_name: str
    last_name: str
    role: str
    is_active: bool
    is_superuser: bool
    is_verified: bool


class UserCreate(schemas.BaseUserCreate):
    email: EmailStr
    password: str
    role: Optional[str] = "Buyer"
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    is_active: Optional[bool] = False
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False


class UserUpdate(schemas.BaseUserUpdate):
    password: Optional[str] = None
    email: Optional[EmailStr] = None
    first_name: Optional[str] = None
    role: Optional[str]
    is_active: Optional[bool] = None
    is_superuser: Optional[bool] = None
    is_verified: Optional[bool] = None


class EmailVerify(BaseModel):
    email: EmailStr
