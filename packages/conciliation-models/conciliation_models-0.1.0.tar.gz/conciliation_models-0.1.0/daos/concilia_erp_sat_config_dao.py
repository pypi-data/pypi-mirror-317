from mongo.core.base_mongo_dao import BaseMongoDAO
from airflow_models.concilia_erp_sat_config import ConciliaErpSatConfig


class ConciliaConfigsDAO(BaseMongoDAO[ConciliaErpSatConfig]): ...
