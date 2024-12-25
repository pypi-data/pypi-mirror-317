from mongo.core.base_mongo_dao import BaseMongoDAO
from mongo.models.customer import Customer


class CustomerDAO(BaseMongoDAO[Customer]): ...
