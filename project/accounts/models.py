from datetime import timedelta, datetime

from sqlalchemy import Column, String, DateTime, Enum, Boolean, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column

from project.db_settings import Base
from fastapi_users.db import SQLAlchemyBaseUserTableUUID


class User(SQLAlchemyBaseUserTableUUID, Base):
    __tablename__ = "user"
    first_name: Mapped[str] = mapped_column(String(length=255), nullable=True)
    last_name: Mapped[str] = mapped_column(String(length=255), nullable=True)
    role: Mapped[Enum] = mapped_column(Enum("Manager", "Buyer", "Consultant", name="user_role"), default="buyer")
    verification_code: Mapped[str] = mapped_column(String(length=255), nullable=True)
    verification_code_expiry: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    email: Mapped[str] = mapped_column(String(length=320), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(length=1024), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    registered_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.utcnow)
