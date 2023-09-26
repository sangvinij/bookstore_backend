from project.accounts.schemas import UserRead

from tests.conftest import user_api

from .conftest import generate_credentials


class TestUpdate:
    def test_user_update_endpoint_inaccessible_for_non_authorized(self, user_data):
        user = user_data["user"]
        email = generate_credentials()["email"]

        failed_rs = user_api.update(user_id=user["id"], superuser_token=None, email=email)

        assert failed_rs.status_code == 401

    def test_user_update_endpoint_inaccessible_for_non_superuser(self, user_data):
        user = user_data["user"]
        token = user_data["token"]
        email = generate_credentials()["email"]

        failed_rs = user_api.update(user_id=user["id"], superuser_token=token, email=email)

        assert failed_rs.status_code == 403

    def test_update_user(self, user_data, superuser_credentials):
        email = generate_credentials()["email"]
        superuser_token = superuser_credentials["superuser_token"]
        user = user_data["user"]
        data = {
            "email": email,
            "first_name": "first name",
            "last_name": "last_name",
            "role": "consultant",
            "is_active": False,
            "is_superuser": True,
            "is_verified": False,
        }

        rs = user_api.update(user_id=user["id"], superuser_token=superuser_token, **data)
        assert rs.status_code == 200

        validated_user = UserRead(**rs.json())

        assert validated_user.email == data["email"]
        assert validated_user.first_name == data["first_name"]
        assert validated_user.last_name == data["last_name"]
        assert validated_user.role == data["role"]
        assert validated_user.is_active == data["is_active"]
        assert validated_user.is_superuser == data["is_superuser"]
        assert validated_user.is_verified == data["is_verified"]

    def test_update_user_with_wrong_role(self, superuser_credentials, user_data):
        superuser_token = superuser_credentials["superuser_token"]
        user = user_data["user"]

        rs = user_api.update(user_id=user["id"], superuser_token=superuser_token, role="wrong_role")

        assert rs.status_code == 400
        assert rs.json()["detail"] == "wrong statement for role"

    def test_update_password(self, superuser_credentials, user_data):
        superuser_token = superuser_credentials["superuser_token"]
        user = user_data["user"]

        password = generate_credentials()["password"]

        rs = user_api.update(user_id=user["id"], superuser_token=superuser_token, password=password)

        assert rs.status_code == 200

        get_user_token_rs = user_api.create_token(email=user["email"], password=password)

        assert get_user_token_rs.status_code == 200
        assert "access_token" in get_user_token_rs.json()
