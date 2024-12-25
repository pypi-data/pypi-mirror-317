from mongo.core.base_mongo_model import BaseMongoModel, mongo_model


@mongo_model(collection_name="tipos_proyecto")
class ProjectType(BaseMongoModel):
    name: str
