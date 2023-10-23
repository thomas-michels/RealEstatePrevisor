from pydantic import BaseModel, Field


class SellingProperty(BaseModel):
    quartos: int = Field(example=2, min=0)
    banheiros: int = Field(example=2, min=0)
    garagens: int = Field(example=2, min=0)
    tamanho: int = Field(example=100, min=0)
    cep: str = Field(example="89012-500", pattern=r"^\d{5}-\d{3}$")
