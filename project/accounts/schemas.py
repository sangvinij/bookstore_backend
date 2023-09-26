import datetime
import uuid
from typing import Optional

from fastapi_users import models as fu_models, schemas

from pydantic import BaseModel, EmailStr


class UserRead(schemas.BaseUser[uuid.UUID]):
    id: fu_models.ID
    email: EmailStr
    first_name: Optional[str]
    last_name: Optional[str]
    role: str
    is_active: bool
    is_superuser: bool
    is_verified: bool
    registered_at: datetime.datetime


class UserCreate(schemas.BaseUserCreate):
    email: EmailStr
    password: str
    role: Optional[str] = "Buyer"
    first_name: Optional[str] = None
    last_name: Optional[str] = None


class UserUpdate(schemas.BaseUserUpdate):
    password: Optional[str] = None
    email: Optional[EmailStr] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    role: Optional[str] = None
    is_active: Optional[bool] = None
    is_superuser: Optional[bool] = None
    is_verified: Optional[bool] = None


class EmailVerify(BaseModel):
    email: EmailStr
