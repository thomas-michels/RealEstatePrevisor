from pydantic import BaseModel, Field, EmailStr, SecretStr


class Login(BaseModel):
    email: EmailStr = Field()
    password: SecretStr = Field()

    class Config:
        allow_population_by_field_name = True
