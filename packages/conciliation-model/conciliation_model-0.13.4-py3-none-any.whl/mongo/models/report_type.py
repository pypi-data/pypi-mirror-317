from mongo.core.base_mongo_model import BaseMongoModel, mongo_model


@mongo_model(collection_name="report_types")
class ReportType(BaseMongoModel):
    name: str
