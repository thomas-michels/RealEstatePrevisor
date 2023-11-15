from app.models import ModelWithHistory, GWOParams, SummarizedModel
from app.configs import get_environment
from typing import List
import requests

_env = get_environment()


class ModelService:
    def get_models(self, page: int, page_size: int) -> List[ModelWithHistory]:
        try:
            print(f"Getting models")
            url = f"{_env.GREY_WOLF_SERVICE_URL}/models"

            params = {"page": page, "page_size": page_size}

            response = requests.get(url=url, params=params)
            print(f"Got models")

            response.raise_for_status()

            return [ModelWithHistory(**model) for model in response.json()]

        except Exception as error:
            print(str(error))
            return []
        
    def get_model_by_id(self, model_id: int) -> SummarizedModel:
        try:
            print(f"Getting model {model_id}")
            url = f"{_env.GREY_WOLF_SERVICE_URL}/models/{model_id}"

            response = requests.get(url=url)
            print("Model got")

            response.raise_for_status()

            return SummarizedModel(**response.json())

        except Exception as error:
            print(str(error))

    def train_new_model(self, name: str, gwo_params: GWOParams) -> SummarizedModel:
        try:
            print("Training new model")
            url = f"{_env.GREY_WOLF_SERVICE_URL}/models/train"

            params = {"name": name}

            response = requests.post(url=url, params=params, json=gwo_params.dict())
            print("Model Train scheduled")

            response.raise_for_status()
            json = response.json()["data"]

            return SummarizedModel(
                id=json["id"],
                name=json["name"],
                status=json["status"],
                created_at=json["created_at"],
                updated_at=json["updated_at"],
            )

        except Exception as error:
            print(str(error))
