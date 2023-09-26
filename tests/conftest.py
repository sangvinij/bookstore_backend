import pytest

from project.env_config import env
from tests.tests_accounts.utils.api_cls import UserAPI

user_api = UserAPI()


@pytest.fixture(scope="session")
def superuser_credentials():
    superuser_email = env.SUPERUSER_EMAIL
    superuser_password = env.SUPERUSER_PASSWORD
    superuser_token = user_api.create_token(superuser_email, superuser_password).json()["access_token"]

    return {
        "superuser_email": superuser_email,
        "superuser_password": superuser_password,
        "superuser_token": superuser_token,
    }
