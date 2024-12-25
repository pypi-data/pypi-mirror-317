from enum import Enum
from typing import Optional, Union

from pydantic import BaseModel, field_validator

from mongo.core.base_mongo_model import BaseMongoModel, mongo_model
from mongo.core.objectid import ObjectId


class Estrategia(Enum):
    JOIN = "join"
    CONCATENATE = "concat"
    ONE_SOURCE = "one_source"


class JoinStrategy(Enum):
    INNER = "inner"
    OUTER = "outer"
    LEFT = "left"
    RIGHT = "right"


class JoinOptions(BaseModel):
    how: JoinStrategy
    left_on: list[str]
    rigth_on: list[str]


class ConcatOptions(BaseModel):
    pass


Options = Union[JoinOptions, ConcatOptions]


class OperacionConfig(BaseModel):
    estrategia: Estrategia
    data_source: ObjectId
    args: Optional[Options] = None


class PipelineConfig(BaseModel):
    ds_base: ObjectId
    operaciones: list[OperacionConfig]


@mongo_model(collection_name="data_erp_config")
class DataERPConfig(BaseMongoModel):
    project_id: ObjectId
    pipeline: PipelineConfig
