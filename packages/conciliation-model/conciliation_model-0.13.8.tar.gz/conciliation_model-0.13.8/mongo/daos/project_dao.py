from mongo.core.base_mongo_dao import BaseMongoDAO
from mongo.models.project import Project


class ProjectDAO(BaseMongoDAO[Project]): ...
