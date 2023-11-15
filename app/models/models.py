from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum


class ModelHistory(BaseModel):
    model_id: int = Field(example=123)
    epoch: int = Field(example=123)
    mse: float = Field(default=1, example=123)
    params: dict = Field(default={})


class ModelHistoryInDB(ModelHistory):
    id: int = Field(example=123)
    created_at: datetime = Field(example=str(datetime.now()))
    updated_at: datetime = Field(example=str(datetime.now()))


class ModelWithHistory(BaseModel):
    id: int = Field(example=123)
    name: Optional[str] = Field(default="", example="test")
    mse: float = Field(default=0, example=123)
    gwo_params: Optional[dict] = Field(default={})
    created_at: datetime = Field(example=str(datetime.now()))
    updated_at: datetime = Field(example=str(datetime.now()))
    history: List[ModelHistoryInDB] = Field(default=[])


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