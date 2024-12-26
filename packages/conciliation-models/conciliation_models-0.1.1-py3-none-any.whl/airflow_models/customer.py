from mongo.core.base_mongo_model import BaseMongoModel, mongo_model


@mongo_model(collection_name="clientes")
class Customer(BaseMongoModel):
    rfc: str
    empresas: list[str]
    nombre_comercial: str
