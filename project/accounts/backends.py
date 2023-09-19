from fastapi_users.authentication.backend import AuthenticationBackend

from fastapi import Response
from fastapi.exceptions import HTTPException
from fastapi_users import models
from fastapi_users.authentication.strategy import Strategy


class CustomAuthenticationBackend(AuthenticationBackend):
    async def login(
            self, strategy: Strategy[models.UP, models.ID], user: models.UP
    ) -> Response:
        if not user.is_verified:
            raise HTTPException(status_code=400, detail="user is not verified")
        token = await strategy.write_token(user)
        return await self.transport.get_login_response(token)
