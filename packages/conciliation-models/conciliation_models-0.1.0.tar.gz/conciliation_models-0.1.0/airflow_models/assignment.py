from pydantic import BaseModel

from mongo.core.base_mongo_model import BaseMongoModel, mongo_model
from mongo.core.objectid import ObjectId


class Header(BaseModel):
    name: str
    data_type: str


@mongo_model(collection_name="asignaciones")
class Assignment(BaseMongoModel):
    datasource_config_id: ObjectId
    name: str
    headerERP: Header  # Cabecera ERP
    headerSAT: Header  # Cabecera SAT
