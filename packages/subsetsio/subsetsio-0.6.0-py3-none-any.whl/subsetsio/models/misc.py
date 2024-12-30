from pydantic import GetCoreSchemaHandler, GetJsonSchemaHandler
from pydantic_core import CoreSchema, core_schema
import re
import typing

class Color(str):
    """Validates hex colors with optional alpha"""
    
    @classmethod
    def __get_pydantic_core_schema__(
        cls,
        _source_type: typing.Any,
        _handler: GetCoreSchemaHandler,
    ) -> CoreSchema:
        return core_schema.no_info_plain_validator_function(cls.validate)

    @classmethod
    def validate(cls, v: str) -> str:
        if not isinstance(v, str):
            raise ValueError("string required")
        
        if not re.match(r'^#[0-9a-fA-F]{6}([0-9a-fA-F]{2})?$', v):
            raise ValueError("invalid hex color format - must be #RRGGBB or #RRGGBBAA")
            
        return v