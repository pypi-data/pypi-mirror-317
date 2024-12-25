from typing import Optional

from pydantic import BaseModel, field_validator

from mongo.daos.report_type_dao import ReportTypeDAO


class HeadersOptions(BaseModel):
    included_headers: Optional[list[str]] = None
    excluded_headers: Optional[list[str]] = None


def get_report_types():
    report_types_dao = ReportTypeDAO()
    report_types_items = report_types_dao.get_all_sync()
    report_types = [item.name for item in report_types_items]
    return report_types


class ReportConfig(BaseModel):
    report_type: str
    headers_options: HeadersOptions
    group_by: Optional[str] = None

    @field_validator("report_type")
    @classmethod
    def validate_report_type(cls, value):
        if value not in get_report_types():
            raise ValueError(f"Report type {value} is not valid")
        return value
