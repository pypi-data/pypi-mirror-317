from enum import Enum
from typing import Annotated, Any

from pydantic import PositiveInt, Field

from mongo.core.base_mongo_model import BaseMongoModel, mongo_model
from mongo.core.objectid import ObjectId
from mongo.pydantic_types.date import Date


class StatusConciliationReport(Enum):
    NO_CONCILIADO = "No conciliado"
    STARTED = "Iniciado"
    FAILED = "Fallido"
    CONCILIADO = "Conciliado"


@mongo_model(collection_name="reportes_conciliacion", schema_version=2)
class ConciliationReport(BaseMongoModel):
    project_id: ObjectId
    name: str
    s3_path: str
    creation_date: Date
    year: PositiveInt
    month: Annotated[PositiveInt, Field(ge=1, le=12)]
    status: StatusConciliationReport = StatusConciliationReport.NO_CONCILIADO
    detail: str = "Reporte no conciliado"
    summary: Any
