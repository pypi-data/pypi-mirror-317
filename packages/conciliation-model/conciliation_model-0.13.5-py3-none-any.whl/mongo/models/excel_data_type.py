from mongo.core.base_mongo_model import BaseMongoModel, mongo_model


@mongo_model(collection_name="excel_data_types")
class ExcelDataType(BaseMongoModel):
    descripcion: str
    formato: str
    ejemplo: str
    nativo: str
