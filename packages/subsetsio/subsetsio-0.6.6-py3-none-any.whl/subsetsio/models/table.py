from typing import List, Literal, Optional, Union
from pydantic import BaseModel, Field
from .base import BaseChart, ChartType

class ColumnConfig(BaseModel):
    label: str = Field(..., min_length=1, max_length=50)
    align: str = Field("left", pattern="^(left|center|right)$")
    width: Optional[int] = None
    format: Optional[str] = None

class TableChartMetadata(BaseChart):
    type: Literal[ChartType.TABLE]
    column_configs: List[ColumnConfig] = Field(
        ...,
        min_items=1,
        description="Configuration for each column in the data array"
    )
    striped: bool = Field(default=True)
    hoverable: bool = Field(default=True)
    page_size: Optional[int] = Field(default=10, ge=1)
    sortable: bool = Field(default=True)

class TableChart(TableChartMetadata):
    data: List[List[Union[str, int, float]]] = Field(
        ...,
        min_items=1,
        description="List of rows, where each row is [value1, value2, ...]"
    )