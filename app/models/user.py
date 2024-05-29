from pydantic import BaseModel, Field, EmailStr
from datetime import datetime


class User(BaseModel):
    id: int = Field(example=123)
    first_name: str = Field(example="First")
    last_name: str = Field(example="Last Name")
    email: EmailStr = Field(example="email@test.com")
    created_at: datetime = Field(example=str(datetime.now()))
    updated_at: datetime = Field(example=str(datetime.now()))
