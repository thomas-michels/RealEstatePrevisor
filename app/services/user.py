from app.configs import get_environment
from app.models.login import Login
from app.models.user import User
from typing import Tuple
import requests
from .base_request_service import BaseRequestService

_env = get_environment()


class UserService(BaseRequestService):

    def __init__(self, token: str) -> None:
        super().__init__(token)
        self.__base_url = _env.GET_IMOVEIS_API_URL

    def login(self, data: Login) -> Tuple[bool, str]:

        url = self.__base_url + "/signin"

        response = requests.post(
            url=url,
            json={
                "email": data.email,
                "password": data.password.get_secret_value()
            }
        )

        json = response.json()

        if response.status_code == 200:
            return True, json
        
        elif response.status_code == 401:
            return False, json["detail"]

        else:
            return False, json["message"]

    def me(self) -> Tuple[bool, User]:
        url = self.__base_url + "/users/me"

        response = requests.get(
            url=url,
            headers=self.get_headers()
        )

        json = response.json()

        if response.status_code == 200:
            return True, User(**json)

        elif response.status_code == 401:
            return False, json["detail"]

        else:
            return False, json.get("message", "Um erro inesperado aconteceu!")
