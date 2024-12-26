from typing import Annotated

from pydantic import Field

from mongo.core.base_mongo_model import BaseMongoModel, mongo_model

RFC_REGEX = r"^[A-Z&Ñ]{3,4}\d{6}[0-9A-Z&Ñ]{3}$"


@mongo_model(collection_name="empresas")
class Company(BaseMongoModel):
    rfc: Annotated[str, Field(pattern=RFC_REGEX)]
    razon_social: str
