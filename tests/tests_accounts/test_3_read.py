from project.accounts.schemas import UserRead

from tests.conftest import user_api
from tests.tests_accounts.utils.schemas import UserList


class TestListRead:
    def test_user_list_endpoint_inaccessible_for_non_authorized(self):
        rs = user_api.get_users_list(superuser_token=None)
        assert rs.status_code == 401

    def test_user_list_endpoint_inaccessible_for_non_superuser(self, user_data):
        token = user_data["token"]
        rs = user_api.get_users_list(superuser_token=token)
        assert rs.status_code == 403

    def test_get_list_users(self, superuser_credentials):
        superuser_token = superuser_credentials["superuser_token"]

        rs = user_api.get_users_list(superuser_token=superuser_token)
        assert rs.status_code == 200

        UserList(**rs.json())

    def test_pagination(self, superuser_credentials, manager, consultant):
        superuser_token = superuser_credentials["superuser_token"]

        rs = user_api.get_users_list(superuser_token=superuser_token, size=1)
        assert rs.status_code == 200

        data = rs.json()

        assert data["total"] >= 3
        assert data["size"] == 1
        assert data["pages"] >= 3
        assert data["page"] == 1

        rs2 = user_api.get_users_list(superuser_token=superuser_token, size=2)
        data2 = rs2.json()

        assert data2["total"] >= 3
        assert data2["size"] == 2
        assert data2["pages"] >= 2
        assert data2["page"] == 1

    def test_filter_by_role(self, superuser_credentials, manager, consultant):
        superuser_token = superuser_credentials["superuser_token"]

        assert consultant["role"] == "consultant"
        assert manager["role"] == "manager"

        rs = user_api.get_users_list(superuser_token=superuser_token, role="buyer")
        data = rs.json()

        assert rs.status_code == 200
        assert all(user["role"] == "buyer" for user in data["items"])

        rs2 = user_api.get_users_list(superuser_token=superuser_token, role="manager")
        data2 = rs2.json()

        assert rs2.status_code == 200
        assert all(user["role"] == "manager" for user in data2["items"])

        rs3 = user_api.get_users_list(superuser_token=superuser_token, role="consultant")
        data3 = rs3.json()

        assert rs3.status_code == 200
        assert all(user["role"] == "consultant" for user in data3["items"])

        rs4 = user_api.get_users_list(superuser_token=superuser_token, role="wrong role")
        assert rs4.status_code == 400
        assert rs4.json()["detail"] == "wrong statement for role"


class TestOneUserRead:
    def test_current_user_endpoint_inaccessible_for_non_authorized(self, user_data):
        failed_rs = user_api.get_update_current_user(method="get", token=None)

        assert failed_rs.status_code == 401

    def test_get_current_user(self, user_data):
        token = user_data["token"]
        email = user_data["email"]

        valid_rs = user_api.get_update_current_user(method="get", token=token)
        user = UserRead(**valid_rs.json())

        assert valid_rs.status_code == 200
        assert user.email == email

    def test_one_user_endpoint_inaccessible_for_non_authorized(self, user_data):
        user = user_data["user"]

        failed_rs = user_api.get_detailed_info_about_user(user_id=user["id"], superuser_token=None)

        assert failed_rs.status_code == 401

    def test_one_user_endpoint_inaccessible_for_non_superuser(self, user_data):
        user = user_data["user"]
        token = user_data["token"]

        failed_rs = user_api.get_detailed_info_about_user(user_id=user["id"], superuser_token=token)

        assert failed_rs.status_code == 403

    def test_get_one_user(self, user_data, superuser_credentials):
        superuser_token = superuser_credentials["superuser_token"]
        user = user_data["user"]

        rs = user_api.get_detailed_info_about_user(user_id=user["id"], superuser_token=superuser_token)
        validated_user = UserRead(**rs.json())

        assert rs.status_code == 200
        assert validated_user.email == user["email"]
