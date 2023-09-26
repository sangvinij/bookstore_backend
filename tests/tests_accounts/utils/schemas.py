from typing import List

from project.accounts.schemas import UserRead

from pydantic import BaseModel


class UserList(BaseModel):
    items: List[UserRead]
    total: int
    page: int
    size: int
    pages: int
