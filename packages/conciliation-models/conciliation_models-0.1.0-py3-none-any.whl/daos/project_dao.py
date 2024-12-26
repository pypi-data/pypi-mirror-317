from mongo.core.base_mongo_dao import BaseMongoDAO
from airflow_models.project import Project


class ProjectDAO(BaseMongoDAO[Project]): ...
