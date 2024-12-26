from mongo.core.base_mongo_dao import BaseMongoDAO
from airflow_models.data_erp_config import DataERPConfig


class DataERPConfigDAO(BaseMongoDAO[DataERPConfig]): ...
