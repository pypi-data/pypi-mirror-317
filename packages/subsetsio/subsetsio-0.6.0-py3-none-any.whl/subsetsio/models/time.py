from pydantic import BaseModel
import re
from typing import Union

class ISODateTime(str):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v, *args, **kwargs):
        if not isinstance(v, str):
            raise ValueError('string required')
        # Matches ISO 8601 datetime with optional timezone
        # e.g., 2024-11-06T22:00:00+00:00 or 2024-11-06T22:00:00Z
        if not re.match(r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:[+-]\d{2}:\d{2}|Z)$', v):
            raise ValueError('invalid ISO datetime format')
        return cls(v)
    
class ISODate(str):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v, *args, **kwargs):
        if not isinstance(v, str):
            raise ValueError('string required')
        if not re.match(r'^\d{4}-\d{2}-\d{2}$', v):
            raise ValueError('invalid ISO date format')
        return cls(v)

class ISOWeek(str):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v, *args, **kwargs):
        if not isinstance(v, str):
            raise ValueError('string required')
        if not re.match(r'^\d{4}-W\d{2}$', v):
            raise ValueError('invalid ISO week format')
        return cls(v)

class Month(str):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v, *args, **kwargs):
        if not isinstance(v, str):
            raise ValueError('string required')
        if not re.match(r'^\d{4}-\d{2}$', v):
            raise ValueError('invalid month format')
        return cls(v)

class Quarter(str):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v, *args, **kwargs):
        if not isinstance(v, str):
            raise ValueError('string required')
        if not re.match(r'^\d{4}-Q[1-4]$', v):
            raise ValueError('invalid quarter format')
        return cls(v)

class Year:
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v: Union[str, int], *args, **kwargs):
        if isinstance(v, str):
            if not re.match(r'^\d{4}$', v):
                raise ValueError('invalid year format')
        else:
            raise ValueError('string or integer required')
        return v

DateType = Union[ISODateTime, ISODate, ISOWeek, Month, Quarter, Year]