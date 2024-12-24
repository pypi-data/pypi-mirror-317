from mongo.core.base_mongo_dao import BaseMongoDAO
from mongo.models.company import Company


class CompanyDAO(BaseMongoDAO[Company]): ...
