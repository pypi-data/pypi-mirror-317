from enum import Enum
from typing import Optional

from pydantic import field_validator

from mongo.core.base_mongo_model import BaseMongoModel, mongo_model
from mongo.daos.excel_data_type_dao import ExcelDataTypeDAO
from mongo.models.datasource_upload import DataSourceType
from mongo.core.objectid import ObjectId


class DatasourceConfigStatus(Enum):
    CREATED = "Created"
    CONFIGURED = "Configured"


@mongo_model(collection_name="datasources_config", schema_version=4)
class DatasourceConfig(BaseMongoModel):
    project_id: ObjectId
    datasource_type: DataSourceType
    datasource_name: str
    header_row: int
    header_types: Optional[dict[str, ObjectId]] = {}
    template_s3_path: Optional[str] = None
    config_status: DatasourceConfigStatus

    @field_validator("header_types")
    @classmethod
    def validate_header_types(cls, v):
        list_data_types = get_avaliable_excel_data_types()
        list_errors = []
        for value in v.values():
            if value not in list_data_types:
                list_errors.append(value)
        if list_errors:
            raise ValueError(
                f"Object_ID de tipo de dato no registrados en cátalogo: {list_errors}"
            )
        return v

    @property
    def is_configured(self) -> bool:
        return bool(self.header_types)

    def update_datasource_config_status(self):
        if not self.is_configured:
            self.config_status = DatasourceConfigStatus.CREATED

        self.config_status = DatasourceConfigStatus.CONFIGURED

        return self


def get_avaliable_excel_data_types():
    excel_data_types = ExcelDataTypeDAO()
    data_types = excel_data_types.get_all_sync()
    data_types = [item.id for item in data_types]
    return data_types
