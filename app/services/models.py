from app.models import ModelWithHistory, GWOParams, SummarizedModel
from app.configs import get_environment
from typing import List
import requests

_env = get_environment()


class ModelService:
    def get_statistics(self) -> dict:
        try:
            url = f"{_env.GREY_WOLF_SERVICE_URL}/models/statistics"

            response = requests.get(url=url)
            print(f"Got statistics")

            response.raise_for_status()

            return response.json()

        except Exception as error:
            print(f"Error on get_statistics: {str(error)}")
            return {}
        
    def delete_model_by_id(self, model_id: int) -> bool:
        try:
            url = f"{_env.GREY_WOLF_SERVICE_URL}/models/{model_id}"

            response = requests.delete(url=url)
            print(f"Model deleted")

            response.raise_for_status()

            return True

        except Exception as error:
            print(f"Error on delete_model_by_id: {str(error)}")
            return False

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

    def get_best_parameters_on_model(self, model_in_db: ModelWithHistory):
        best_params = {}
        best_mae = 1

        for history in model_in_db.history:

            if history.mae < best_mae:
                best_params = history.dict()
                best_mae = history.mae

        return best_params
