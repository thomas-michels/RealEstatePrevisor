from typing import List, Optional
from pydantic import BaseModel, Field, validator
from datetime import datetime
from enum import Enum


class ModelHistory(BaseModel):
    model_id: int = Field(example=123)
    epoch: int = Field(example=123)
    mae: float = Field(default=1, example=123, alias="mse")
    params: dict = Field(default={})

    @validator("mae", always=True, allow_reuse=True)
    def validator_mae(cls, value: float):
        return round(value, 5)

    class Config:
        allow_population_by_field_name = True


class ModelHistoryInDB(ModelHistory):
    id: int = Field(example=123)
    created_at: datetime = Field(example=str(datetime.now()))
    updated_at: datetime = Field(example=str(datetime.now()))


class ModelWithHistory(BaseModel):
    id: int = Field(example=123)
    name: Optional[str] = Field(default="", example="test")
    mae: float = Field(default=0, example=123, alias="mse")
    gwo_params: Optional[dict] = Field(default={})
    created_at: datetime = Field(example=str(datetime.now()))
    updated_at: datetime = Field(example=str(datetime.now()))
    history: List[ModelHistoryInDB] = Field(default=[])

    @validator("mae", always=True, allow_reuse=True)
    def validator_mae(cls, value: float):
        return round(value, 5)

    class Config:
        allow_population_by_field_name = True


class ModelStatus(str, Enum):
    SCHEDULED: str = "SCHEDULED"
    TRAINING: str = "TRAINING"
    READY: str = "READY"
    ERROR: str = "ERROR"


class SummarizedModel(BaseModel):
    id: int = Field(example=123)
    name: str = Field(default="", example="test")
    status: ModelStatus = Field(
        default=ModelStatus.SCHEDULED, example=ModelStatus.SCHEDULED
    )
    remaining_time_in_seconds: Optional[float] = Field(default=0)
    created_at: datetime = Field(example=str(datetime.now()))
    updated_at: datetime = Field(example=str(datetime.now()))
