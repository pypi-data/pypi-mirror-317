from mongo.core.base_mongo_dao import BaseMongoDAO
from mongo.models.conciliation_report import ConciliationReport


class ConciliationReportDAO(BaseMongoDAO[ConciliationReport]): ...
