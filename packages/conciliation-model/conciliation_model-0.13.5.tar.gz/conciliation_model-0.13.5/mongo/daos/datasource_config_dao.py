from mongo.core.base_mongo_dao import BaseMongoDAO
from mongo.models.datasource_config import DatasourceConfig

class DatasourceConfigsDAO(BaseMongoDAO[DatasourceConfig]): ...
