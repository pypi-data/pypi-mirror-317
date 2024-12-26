from mongo.core.base_mongo_dao import BaseMongoDAO
from airflow_models.excel_data_type import ExcelDataType


class ExcelDataTypeDAO(BaseMongoDAO[ExcelDataType]): ...
