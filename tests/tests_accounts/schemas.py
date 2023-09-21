from typing import List

from pydantic import BaseModel
from project.accounts.schemas import UserRead


class UserList(BaseModel):
    items: List[UserRead]
    total: int
    page: int
    size: int
    pages: int
