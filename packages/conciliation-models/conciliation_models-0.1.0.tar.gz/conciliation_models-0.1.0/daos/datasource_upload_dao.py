from mongo.core.base_mongo_dao import BaseMongoDAO
from airflow_models.datasource_upload import DatasourceUpload



class DatasourceUploadDAO(BaseMongoDAO[DatasourceUpload]): ...
