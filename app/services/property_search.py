import requests
from requests.exceptions import ConnectionError
from app.configs import get_environment

_env = get_environment()

class PropertySearch:

    def find_similar_properties(
        self,
        page_size: int,
        offset: int,
        rooms: int=0,
        bathrooms: int=0,
        parking_space: int=0,
        size: int=0,
        zip_code: str=""
    ):
        url = f"{_env.PROPERTIES_API_URL}/properties"
        params = {"page_size": page_size, "offset": offset}

        if rooms:
            params["rooms"] = rooms

        if bathrooms:
            params["bathrooms"] = bathrooms

        if parking_space:
            params["parking_space"] = parking_space

        if size:
            params["size"] = size

        if zip_code:
            params["zip_code"] = zip_code
        try:
            response = requests.get(url=url, params=params)

        except ConnectionError:
            return "Serviço indisponivel!"

        if response.status_code == 404:
            return "Nenhuma propriedade encontrada, tente outros filtros!"
        
        elif response.status_code == 200:
        
            all_properties = {}

            json = response.json().get("data", [])

            for property in json:
                all_properties[f'{float(property["latitude"])}-{float(property["longitude"])}'] = property

            return json

        else:
            return "Serviço indisponivel no momento, tente mais tarde!"
