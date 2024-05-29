from pydantic import BaseModel, Field, SecretStr


class UpdateUser(BaseModel):
    new_password: SecretStr = Field()
    confirm_password: SecretStr = Field()

    class Config:
        allow_population_by_field_name = True
