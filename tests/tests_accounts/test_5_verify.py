from tests.conftest import user_api


class TestVerify:
    def test_get_verification_link(self, user_data):
        user = user_data["user"]

        rs = user_api.get_verification_link(email=user["email"])

        assert rs.status_code == 200
        assert "url" in rs.json()

    def test_verify_email(self, user_data, superuser_credentials):
        superuser_token = superuser_credentials["superuser_token"]
        user = user_data["user"]

        get_verification_token_rs = user_api.get_verification_link(email=user["email"])

        verification_token = get_verification_token_rs.json()["token"]

        failed_verify_rs = user_api.verify(user_id=user["id"], verification_token=verification_token)

        assert failed_verify_rs.status_code == 400
        assert failed_verify_rs.json()["detail"] == "user already verified"

        update_is_verified_rs = user_api.update(user_id=user["id"], superuser_token=superuser_token, is_verified=False)
        assert update_is_verified_rs.json()["is_verified"] is False

        valid_verify_rs = user_api.verify(user_id=user["id"], verification_token=verification_token)
        assert valid_verify_rs.status_code == 200

        assert valid_verify_rs.json()["detail"] == "user successfully verified"

        check_verified_status_rs = user_api.get_detailed_info_about_user(user_id=user["id"],
                                                                         superuser_token=superuser_token)

        assert check_verified_status_rs.json()["is_verified"]

    def test_verify_with_wrong_token(self, user_data):
        user = user_data["user"]

        failed_verify_rs = user_api.verify(user_id=user["id"], verification_token="wrong_token")
        assert failed_verify_rs.status_code == 404
        assert failed_verify_rs.json()["detail"] == "invalid link"
