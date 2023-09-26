import uuid

from project.env_config import env

import requests


class UserAPI:
    ENDPOINT = f"{env.HOST_FOR_TESTS}/auth/users"
    timeout = 30

    def create(self, email: str, password: str, **kwargs) -> requests.models.Response:
        data = {"email": email, "password": password, **kwargs}
        rs = requests.post(f"{self.ENDPOINT}/register", json=data, timeout=self.timeout)
        return rs

    def create_token(self, email, password) -> requests.models.Response:
        rs = requests.post(
            f"{self.ENDPOINT}/login", data={"username": email, "password": password}, timeout=self.timeout
        )
        return rs

    def get_update_current_user(self, token: str, method: str = "get", **kwargs) -> requests.models.Response:
        url = f"{self.ENDPOINT}/me"
        headers = {"Authorization": f"Bearer {token}"}
        match method:
            case "get":
                rs = requests.get(url=url, headers=headers, timeout=self.timeout)
            case "update":
                rs = requests.patch(url=url, headers=headers, json=kwargs, timeout=self.timeout)
            case _:
                raise TypeError("wrong method")

        return rs

    def update(self, superuser_token: str, user_id: uuid.UUID, **kwargs) -> requests.models.Response:
        headers = {"Authorization": f"Bearer {superuser_token}"}

        rs = requests.patch(f"{self.ENDPOINT}/{user_id}", json=kwargs, headers=headers, timeout=self.timeout)

        return rs

    def get_detailed_info_about_user(self, user_id: uuid.UUID, superuser_token: str) -> requests.models.Response:
        rs = requests.get(
            f"{self.ENDPOINT}/{user_id}", headers={"Authorization": f"Bearer {superuser_token}"}, timeout=self.timeout
        )
        return rs

    def delete(self, user_id: uuid.UUID, superuser_token: str) -> requests.models.Response:
        rs = requests.delete(
            f"{self.ENDPOINT}/{user_id}", headers={"Authorization": f"Bearer {superuser_token}"}, timeout=self.timeout
        )
        return rs

    def get_users_list(self, superuser_token: str, **params) -> requests.models.Response:
        rs = requests.get(
            f"{self.ENDPOINT}",
            params=params,
            headers={"Authorization": f"Bearer {superuser_token}"},
            timeout=self.timeout,
        )
        return rs

    def get_verification_link(self, email: str) -> requests.models.Response:
        rs = requests.post(f"{self.ENDPOINT}/verify_email", json={"email": email}, timeout=self.timeout)
        return rs

    def verify(self, user_id, verification_token) -> requests.models.Response:
        rs = requests.get(f"{self.ENDPOINT}/{user_id}/verify_email/{verification_token}", timeout=self.timeout)

        return rs
