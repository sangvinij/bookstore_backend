import uuid
from datetime import datetime, timedelta

from asyncpg.exceptions import InvalidTextRepresentationError
from fastapi import HTTPException

from fastapi_users import exceptions, models, schemas
from typing import Optional

from fastapi_users import BaseUserManager, UUIDIDMixin
from fastapi import Depends, Request

from project.accounts.auth import get_user_db
from project.accounts.models import User
from project.accounts.utils import hash_verification_code, get_verification_url, \
    generate_verification_code, send_verification_email
from project.config import VERIFICATION_CODE_TTL

class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):

    async def create(
            self,
            user_create: schemas.UC,
            safe: bool = False,
            request: Optional[Request] = None,
    ) -> models.UP:
        await self.validate_password(user_create.password, user_create)

        existing_user = await self.user_db.get_by_email(user_create.email)

        if existing_user is not None:
            raise exceptions.UserAlreadyExists()

        user_dict = (
            user_create.create_update_dict()
            if safe
            else user_create.create_update_dict_superuser()
        )
        password = user_dict.pop("password")
        user_dict["hashed_password"] = self.password_helper.hash(password)
        user_dict["role"] = "Buyer"

        created_user = await self.user_db.create(user_dict)
        try:
            await self.on_after_register(created_user, request)

        except Exception:
            await self.user_db.delete(created_user)
            raise HTTPException(status_code=500, detail="error while sending a message")

        return created_user

    async def on_after_register(
            self, user: models.UP,
            request: Optional[Request] = None,
    ):
        if not user.is_verified:
            token = generate_verification_code()
            verification_code = hash_verification_code(token)
            url = get_verification_url(user.id, token)

            await self.user_db.update(user, update_dict={"verification_code": verification_code,
                                                         "verification_code_expiry": VERIFICATION_CODE_TTL})

            await send_verification_email(user, url)

    async def update(
        self,
        user_update: schemas.UU,
        user: models.UP,
        safe: bool = False,
        request: Optional[Request] = None,
    ) -> models.UP:

        if safe:
            updated_user_data = user_update.create_update_dict()
        else:
            updated_user_data = user_update.create_update_dict_superuser()

        if "role" in updated_user_data and updated_user_data["role"] not in ("Buyer", "Consultant", "Manager"):
            raise HTTPException(status_code=400, detail="wrong statement for role")

        updated_user = await self._update(user, updated_user_data)


        return updated_user


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)
