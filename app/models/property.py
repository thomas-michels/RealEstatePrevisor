from pydantic import BaseModel, Field


class SellingProperty(BaseModel):
    quartos: int = Field(example=2, min=0)
    banheiros: int = Field(example=2, min=0)
    garagens: int = Field(example=2, min=0)
    tamanho: int = Field(example=100, min=0)
    cep: str = Field(example="89066-040", pattern=r"^\d{5}-\d{3}$")


class Property(BaseModel):
    rooms: int = Field(example=2)
    bathrooms: int = Field(example=2)
    parking_space: int = Field(example=2)
    size: int = Field(example=100)
    neighborhood_name: str = Field(example="viktor konder")
    flood_quota: float = Field(default=None)


class PredictedProperty(BaseModel):
    property: Property
    predicted_price: float = Field(example=123)
    mse: float = Field(example=123)
