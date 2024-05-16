
import requests
from app.configs import get_environment
from app.models import SellingProperty, PredictedProperty

_env = get_environment()

def predict_property_price(model_id: int, property: SellingProperty) -> PredictedProperty:

    try:
        url = f"{_env.GET_IMOVEIS_API_URL}/properties/price/predict"

        if not property.cep.__contains__("-"):
            zip_code = list(property.cep)
            zip_code.insert(-3, "-")
            property.cep = "".join(zip_code)

        body = {
            "rooms": property.quartos,
            "bathrooms": property.banheiros,
            "parking_space": property.garagens,
            "size": property.tamanho,
            "zip_code": property.cep,
        }

        params = {"model_id": model_id}

        response = requests.post(url=url, json=body, params=params)

        if response.status_code == 200:
            json = response.json()
            return PredictedProperty(
                predicted_price=json["predicted_price"],
                mae=json["mse"],
                property=json["property"],
            )
        
        elif response.status_code == 404:
            return "Os dados fornecidos são inválidos!"
        
        return "Serviço de previsão de preços indisponivel, tente novamente mais tarde!"
    
    except Exception as error:
        raise Exception("Serviço de previsão de preços indisponivel, tente novamente mais tarde!")
