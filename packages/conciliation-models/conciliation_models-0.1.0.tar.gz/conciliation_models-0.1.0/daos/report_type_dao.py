from mongo.core.base_mongo_dao import BaseMongoDAO
from airflow_models.report_type import ReportType


class ReportTypeDAO(BaseMongoDAO[ReportType]): ...
