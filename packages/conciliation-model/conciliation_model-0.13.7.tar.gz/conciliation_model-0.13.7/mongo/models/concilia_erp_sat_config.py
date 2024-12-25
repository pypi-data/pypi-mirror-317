from enum import Enum
from typing import Optional

from pydantic import BaseModel

from mongo.core.base_mongo_model import BaseMongoModel, mongo_model
from mongo.core.objectid import ObjectId


class EstrategiaConcilia(Enum):
    UUID = "uuid"
    SERIE = "serie"
    FOLIO = "folio"
    SERIE_FOLIO = "serie-folio"
    CUSTOM = "custom"


class Options(Enum):
    CONCAT = "concat"
    REGEX = "regex"


class PivoteConfig(BaseModel):
    columns: list[str]
    estrategia: EstrategiaConcilia
    args: Optional[Options] = None


@mongo_model(collection_name="concilia_erp_sat_config")
class ConciliaErpSatConfig(BaseMongoModel):
    project_id: ObjectId
    pivotes: list[PivoteConfig]
