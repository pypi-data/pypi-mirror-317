from mongo.core.base_mongo_dao import BaseMongoDAO
from airflow_models.customer import Customer


class CustomerDAO(BaseMongoDAO[Customer]): ...
