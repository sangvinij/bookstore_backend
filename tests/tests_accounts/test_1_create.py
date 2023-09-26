from project.accounts.schemas import UserRead

from tests.conftest import user_api

from .conftest import generate_credentials


class TestCreate:
    email, password = generate_credentials().values()

    def test_create_user(self, superuser_credentials):
        superuser_token = superuser_credentials["superuser_token"]
        rs = user_api.create(
            email=self.email,
            password=self.password,
            first_name="test_name",
            last_name="test_last_name",
            role="buyer",
        )

        assert rs.status_code == 201
        created_user_data = rs.json()

        user = UserRead(**created_user_data)

        assert user.email == self.email
        assert user.first_name == "test_name"
        assert user.last_name == "test_last_name"
        assert user.role == "buyer"
        assert user.is_active
        assert not user.is_superuser
        assert not user.is_verified

        rs2 = user_api.delete(user.id, superuser_token=superuser_token)
        assert rs2.status_code == 204

    def test_create_user_with_only_mandatory_fields(self, superuser_credentials):
        superuser_token = superuser_credentials["superuser_token"]
        create_rs = user_api.create(
            email=self.email,
            password=self.password,
        )
        assert create_rs.status_code == 201

        delete_rs = user_api.delete(create_rs.json()["id"], superuser_token=superuser_token)
        assert delete_rs.status_code == 204

    def test_create_user_with_wrong_role(self, superuser_credentials):
        superuser_token = superuser_credentials["superuser_token"]
        rs = user_api.create(
            email=self.email,
            password=self.password,
            role="wrong role",
        )

        assert rs.status_code == 201

        user = UserRead(**rs.json())

        assert user.email == self.email
        assert user.role == "buyer"

        rs2 = user_api.delete(user.id, superuser_token=superuser_token)
        assert rs2.status_code == 204
