import random
import string

import pytest

from tests.conftest import user_api


def generate_credentials():
    email = "test." + "".join(random.choices(string.ascii_lowercase, k=6)) + '@example.com'
    password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
    return {"email": email, "password": password}


@pytest.fixture()
def user_data(superuser_credentials):
    superuser_token = superuser_credentials["superuser_token"]

    email, password = generate_credentials().values()
    user = user_api.create(email, password).json()

    # verify user
    user_api.update(user_id=user["id"], superuser_token=superuser_token, is_verified=True)

    token = user_api.create_token(email, password).json()["access_token"]

    yield {"user": user, "email": email, "password": password, "token": token}

    user_api.delete(user_id=user["id"], superuser_token=superuser_token)


@pytest.fixture()
def consultant(superuser_credentials):
    superuser_token = superuser_credentials["superuser_token"]
    email, password = generate_credentials().values()

    user = user_api.create(email, password).json()

    consultant = user_api.update(user_id=user["id"], superuser_token=superuser_token,
                                 is_verified=True, role="consultant").json()

    yield consultant

    user_api.delete(user_id=user["id"], superuser_token=superuser_token)


@pytest.fixture()
def manager(superuser_credentials):
    superuser_token = superuser_credentials["superuser_token"]
    email, password = generate_credentials().values()

    user = user_api.create(email, password).json()

    manager = user_api.update(user_id=user["id"], superuser_token=superuser_token,
                              is_verified=True, role="manager").json()

    yield manager

    user_api.delete(user_id=user["id"], superuser_token=superuser_token)
