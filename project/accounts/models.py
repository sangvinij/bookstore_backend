from typing import List

from sqlalchemy import Column, String

from project.db_settings import Base
from fastapi_users.db import SQLAlchemyBaseUserTableUUID, SQLAlchemyUserDatabase, SQLAlchemyBaseOAuthAccountTableUUID
from sqlalchemy.orm import Mapped, relationship
import shortuuid


class OAuthAccount(SQLAlchemyBaseOAuthAccountTableUUID, Base):
    pass


class User(SQLAlchemyBaseUserTableUUID, Base):
    __tablename__ = "user"
    username = Column(String, unique=True, nullable=False, default=shortuuid.uuid)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    oauth_accounts: Mapped[List[OAuthAccount]] = relationship(
        "OAuthAccount", lazy="joined"
    )
