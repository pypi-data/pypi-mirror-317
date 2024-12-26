import re
from typing import Any

from pydantic import GetCoreSchemaHandler, GetJsonSchemaHandler
from pydantic.json_schema import JsonSchemaValue
from pydantic_core import core_schema

RFC_REGEX = r"^[A-Z&Ñ]{3,4}\d{6}[0-9A-Z&Ñ]{3}$"


class RFC(str):
    @classmethod
    def __get_pydantic_core_schema__(
        cls,
        _source_type: Any,
        _handler: GetCoreSchemaHandler,
    ) -> core_schema.CoreSchema:

        def validate_rfc(rfc: str):
            if not re.match(RFC_REGEX, rfc):
                raise ValueError(
                    f"'{rfc}' no es un RFC válido, por favor proporcione un RFC válido."
                )
            return rfc

        rfc_schema = core_schema.no_info_plain_validator_function(validate_rfc)

        schema = core_schema.json_or_python_schema(
            json_schema=core_schema.str_schema(pattern=RFC_REGEX),
            python_schema=rfc_schema,
        )

        return schema

    @classmethod
    def __get_pydantic_json_schema__(
        cls, _core_schema: core_schema.CoreSchema, handler: GetJsonSchemaHandler
    ) -> JsonSchemaValue:
        schema = handler(core_schema.str_schema(pattern=RFC_REGEX))
        return schema
