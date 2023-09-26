from tests.conftest import user_api

from .conftest import generate_credentials


class TestLogin:
    email, password = generate_credentials()

    def test_get_token_with_wrong_and_correct_data(self, user_data, superuser_credentials):
        email = user_data["email"]
        password = user_data["password"]

        failed_login_rs = user_api.create_token(email=email, password=f"wrong {password}")
        assert failed_login_rs.status_code == 400
        assert "access_token" not in failed_login_rs.json()

        valid_login_rs = user_api.create_token(email=email, password=password)
        assert valid_login_rs.status_code == 200
        assert "access_token" in valid_login_rs.json()

    def test_login_unverified(self, user_data, superuser_credentials):
        superuser_token = superuser_credentials["superuser_token"]
        email = user_data["email"]
        password = user_data["password"]
        user_id = user_data["user"]["id"]

        update_is_verify_status_rs = user_api.update(
            user_id=user_id, superuser_token=superuser_token, is_verified=False
        )

        assert update_is_verify_status_rs.status_code == 200
        assert update_is_verify_status_rs.json()["is_verified"] is False

        login_rs = user_api.create_token(email=email, password=password)

        assert login_rs.status_code == 400
        assert login_rs.json()["detail"] == "user is not verified"

    def test_get_access_to_protected_endpoint(self, user_data):
        token = user_data["token"]
        email = user_data["email"]

        failed_rs = user_api.get_update_current_user(method="get", token="wrong token")
        assert failed_rs.status_code == 401

        valid_rs = user_api.get_update_current_user(method="get", token=token)

        assert valid_rs.status_code == 200
        assert valid_rs.json()["email"] == email

    def test_login_with_spaces_in_credentials(self, user_data):
        email = user_data["email"]
        password = user_data["password"]

        rs = user_api.create_token(email=f" {email}", password=password)
        assert rs.status_code == 400

        rs2 = user_api.create_token(email=f"{email} ", password=password)
        assert rs2.status_code == 400

        rs3 = user_api.create_token(email=email, password=f" {password}")
        assert rs3.status_code == 400

        rs4 = user_api.create_token(email=email, password=f"{password} ")
        assert rs4.status_code == 400

        valid_rs = user_api.create_token(email=email, password=password)
        assert valid_rs.status_code == 200
        assert "access_token" in valid_rs.json()
