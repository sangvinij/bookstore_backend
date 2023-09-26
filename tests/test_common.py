from tests.conftest import user_api


class TestCommon:
    def test_superuser_exists(self, superuser_credentials):
        superuser_token = superuser_credentials["superuser_token"]
        superuser_email = superuser_credentials["superuser_email"]

        rs = user_api.get_update_current_user(method="get", token=superuser_token)

        assert rs.status_code == 200
        assert rs.json()["email"] == superuser_email
