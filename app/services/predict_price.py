
import requests
from app.configs import get_environment
from app.models import SellingProperty, PredictedProperty

_env = get_environment()

def predict_property_price(property: SellingProperty) -> PredictedProperty:

    try:
        url = f"{_env.PROPERTIES_API_URL}/properties/price/predict"

        body = {
            "rooms": property.quartos,
            "bathrooms": property.banheiros,
            "parking_space": property.garagens,
            "size": property.tamanho,
            "zip_code": property.cep,
        }

        response = requests.post(url=url, json=body)

        if response.status_code == 200:
            return PredictedProperty(**response.json())
        
        elif response.status_code == 404:
            return "Os dados fornecidos são inválidos!"
        
        return "Serviço de previsão de preços indisponivel, tente novamente mais tarde!"
    
    except Exception as error:
        raise Exception("Serviço de previsão de preços indisponivel, tente novamente mais tarde!")
