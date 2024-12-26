from mongo.core.base_mongo_dao import BaseMongoDAO
from airflow_models.company import Company


class CompanyDAO(BaseMongoDAO[Company]): ...
