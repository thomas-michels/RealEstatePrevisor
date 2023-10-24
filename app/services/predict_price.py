
import requests
from app.configs import get_environment
from app.models import SellingProperty, PredictedProperty

_env = get_environment()

def predict_property_price(property: SellingProperty) -> PredictedProperty:

    try:
        url = f"{_env.PROPERTIES_API_URL}/properties/predict"

        response = requests.post(url=url, json=property.dict())

        response.raise_for_status()

        return PredictedProperty(**response.json())
    
    except Exception as error:
        raise Exception("Serviço de previsão de preços indisponivel, tente novamente mais tarde!")
