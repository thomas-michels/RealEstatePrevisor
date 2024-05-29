
class BaseRequestService:

    def __init__(self, token: str) -> None:
        self.token = token

    def set_token(self, new_token: str) -> None:
        self.token = new_token

    def get_headers(self) -> dict:
        return {
            "Authorization": self.token
        }
