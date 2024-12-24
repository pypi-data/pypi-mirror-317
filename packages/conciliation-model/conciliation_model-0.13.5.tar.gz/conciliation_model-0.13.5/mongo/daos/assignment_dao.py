from mongo.core.base_mongo_dao import BaseMongoDAO
from mongo.models.assignment import Assignment


class AssignmentDAO(BaseMongoDAO[Assignment]): ...
