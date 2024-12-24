from enum import Enum
from typing import Annotated, Optional

from pydantic import BaseModel, Field, field_validator, model_validator

from mongo.core.base_mongo_model import BaseMongoModel, mongo_model
from mongo.daos.datasource_config_dao import DatasourceConfigsDAO
from mongo.daos.project_type_dao import ProjectTypeDAO
from mongo.models.report_config import ReportConfig
from mongo.pydantic_types.date import Date
from mongo.pydantic_types.rfc_str import RFC_REGEX


def get_available_project_types():
    project_types_dao = ProjectTypeDAO()
    project_types_items = project_types_dao.get_all_sync()
    project_types = [item.name for item in project_types_items]
    return project_types


class Trigger(Enum):
    MANUAL = "Manual"  # cuando se ejecuta manualmente
    SCHEDULED = "Scheduled"  # cuando se programa la ejecución
    AUTOMATIC = "Automatic"  # cuando se suben los archivos


class ScheduleConfig(BaseModel):
    day_of_month: int


class ProjectStatus(Enum):
    ACTIVE = "Activo"
    INACTIVE = "Inactivo"
    DELETED = "Eliminado"


class ProjectConfigurationStatus(Enum):
    INITIAL_CONFIG = "Initial config"
    DATASOURCE_CONFIG = "Datasource config"
    COMPLETED = "Completed"


@mongo_model(collection_name="proyectos", schema_version=4)
class Project(BaseMongoModel):
    name: str
    owner: str  # Nombre comercial del cliente propietario del proyecto
    owner_rfc: Annotated[str, Field(pattern=RFC_REGEX)]
    project_type: str
    enterprises: list[str]
    start_date: Date
    end_date: Date
    trigger: list[Trigger]
    report_config: ReportConfig
    schedule_config: Optional[ScheduleConfig] = None
    project_status: ProjectStatus
    configuration_status: ProjectConfigurationStatus = (
        ProjectConfigurationStatus.INITIAL_CONFIG
    )

    @property
    async def datasources_config(self):
        if self.id is None:
            raise ValueError(
                "Project must be saved in database to get datasources config"
            )

        datasource_config_dao = DatasourceConfigsDAO()
        return await datasource_config_dao.get_all(project_id=self.id)

    @field_validator("project_type")
    @classmethod
    def validate_project_type(cls, value):
        if value not in get_available_project_types():
            raise ValueError(f"Project type {value} is not valid")
        return value

    @model_validator(mode="after")
    def validate_schedule_config(self):
        if Trigger.SCHEDULED in self.trigger and self.schedule_config is None:
            raise ValueError("Schedule config is required for scheduled projects")

        if Trigger.SCHEDULED not in self.trigger and self.schedule_config is not None:
            raise ValueError(
                "Schedule config is not allowed for non-scheduled projects"
            )

        return self

    async def update_configuration_status(self, datasources_config):
        if not datasources_config:
            self.configuration_status = ProjectConfigurationStatus.INITIAL_CONFIG
        elif all(
            datasource_config.is_configured for datasource_config in datasources_config
        ):
            self.configuration_status = ProjectConfigurationStatus.COMPLETED
        else:
            self.configuration_status = ProjectConfigurationStatus.DATASOURCE_CONFIG

        return self
