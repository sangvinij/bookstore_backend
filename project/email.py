from typing import List

from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType
from pydantic import BaseModel, EmailStr

from project.env_config import env


class EmailSchema(BaseModel):
    email: List[EmailStr]


conf = ConnectionConfig(
    MAIL_USERNAME=env.MAIL_USERNAME,
    MAIL_PASSWORD=env.MAIL_PASSWORD,
    MAIL_FROM=env.MAIL_FROM,
    MAIL_PORT=env.MAIL_PORT,
    MAIL_SERVER=env.MAIL_SERVER,
    SUPPRESS_SEND=env.SUPPRESS_SEND,
    MAIL_STARTTLS=False,
    MAIL_SSL_TLS=True,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
)
