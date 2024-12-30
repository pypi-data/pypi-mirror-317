from pydantic import BaseModel, Field, field_validator
from typing import List, Literal, Optional, Union
from .base import BaseChart, ChartType
from .misc import Color

class MapChartMetadata(BaseChart):
    type: Literal[ChartType.MAP]
    low_value_color: Color = Field(default=Color("#FFFFFF"))
    high_value_color: Color = Field(default=Color("#00FF00"))

class MapChart(MapChartMetadata):
    data: List[List[Union[str, float]]] = Field(
        ...,
        min_items=1,
        description="List of data points, where each point is [country_code, value]"
    )

    @field_validator('data')
    def validate_country_codes(cls, v):
        for point in v:
            country_code = point[0]
            if not (len(country_code) == 2 and country_code.isalpha() and country_code.isupper()):
                raise ValueError("Country must be a 2-letter uppercase code")
        return v