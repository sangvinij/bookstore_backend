import hashlib
import secrets
import uuid

from fastapi_mail import FastMail, MessageSchema

from project.email import conf
from project.env_config import env

from .models import User


def generate_verification_code(length: int = 32) -> str:
    token = secrets.token_hex(length)
    return token


def hash_verification_code(token, algorithm: str = "sha256") -> str:
    hasher = hashlib.new(algorithm)
    hasher.update(token.encode("utf-8"))
    hashed_token = hasher.hexdigest()
    return hashed_token


def get_verification_url(user_id: uuid.UUID, token: str) -> str:
    url = f"{env.WEBAPP_HOST}/auth/users/{user_id}/verify_email/{token}"
    return url


async def send_verification_email(user: User, url: str):
    message = MessageSchema(
        subject="Verification", recipients=[user.email], body=f"Please verify your email: {url}", subtype="plain"
    )
    mail = FastMail(conf)

    await mail.send_message(message)
