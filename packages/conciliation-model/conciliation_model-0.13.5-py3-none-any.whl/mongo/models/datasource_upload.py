import io
from enum import Enum
from typing import Type

import httpx
from pydantic import NonNegativeInt, PositiveInt

from s3.files.bucket_manager import BucketManager
from mongo.core.base_mongo_model import BaseMongoModel, mongo_model
from mongo.core.objectid import ObjectId
from tools.datasources.abc_datasource import DataSource
from tools.datasources.csv_datasource import CsvDatasource
from tools.datasources.excel_datasource import ExcelDataSource
from mongo.pydantic_types.date import Date


class DataSourceType(Enum):
    EXCEL = "EXCEL"
    CSV = "CSV"

    @property
    def ds_class(self) -> Type[ExcelDataSource | CsvDatasource]:
        return DATASOURCE_TYPES[self]

    @property
    def allowed_file_extensions(self) -> list[str]:
        if self == DataSourceType.EXCEL:
            return ["xls", "xlsx"]
        if self == DataSourceType.CSV:
            return ["csv"]
        raise ValueError(f"Unknown DataSourceType: {self}")


DATASOURCE_TYPES: dict[DataSourceType, Type[ExcelDataSource | CsvDatasource]] = {
    DataSourceType.EXCEL: ExcelDataSource,
    DataSourceType.CSV: CsvDatasource,
}


class DatasourceUploadStatus(Enum):
    PENDING = "Pendiente"
    UPLOADED = "Cargado"


@mongo_model(collection_name="datasource_uploads", schema_version=2)
class DatasourceUpload(BaseMongoModel):
    datasource_config_id: ObjectId
    type: DataSourceType
    s3_path: str
    header_row: NonNegativeInt = 0
    month: PositiveInt
    year: PositiveInt
    uploaded_by: str
    upload_date: Date

    @property
    def datasource(self) -> DataSource:
        bucket_manager = BucketManager()

        file_url = bucket_manager.create_presigned_url(self.s3_path)

        response = httpx.get(file_url)
        response.raise_for_status()
        binary_io = io.BytesIO(response.content)

        return self.type.ds_class(binary_io, self.header_row)
