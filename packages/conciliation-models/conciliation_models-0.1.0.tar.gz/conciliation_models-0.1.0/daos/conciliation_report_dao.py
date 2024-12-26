from mongo.core.base_mongo_dao import BaseMongoDAO
from airflow_models.conciliation_report import ConciliationReport


class ConciliationReportDAO(BaseMongoDAO[ConciliationReport]): ...
