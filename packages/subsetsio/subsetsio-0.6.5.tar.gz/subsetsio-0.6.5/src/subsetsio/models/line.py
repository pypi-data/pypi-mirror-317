from enum import Enum
from pydantic import BaseModel, Field
from typing import List, Literal, Optional, Union
from .time import DateType
from .misc import Color
from .base import BaseChart, ChartType

class LineStyle(str, Enum):
    SOLID = "solid"
    DASHED = "dashed"
    DOTTED = "dotted"

class DatasetConfig(BaseModel):
    label: str = Field(..., min_length=1, max_length=50, description="Label for this dataset")
    line_style: LineStyle = Field(default=LineStyle.SOLID)
    color: Color = Field(default="#000000")
    point_size: int = Field(default=4, ge=2, le=10)

class AxisConfig(BaseModel):
    label: str = Field(..., min_length=1, max_length=50)
    show_grid: bool = Field(default=True)
    show_line: bool = Field(default=True)

class YAxisConfig(AxisConfig):
    min: Optional[float] = None
    max: Optional[float] = None
    log_scale: bool = Field(default=False)

class LineChartMetadata(BaseChart):
    type: Literal[ChartType.LINE]
    dataset_configs: List[DatasetConfig] = Field(..., min_items=1, max_items=10)
    x_axis: AxisConfig
    y_axis: YAxisConfig
    show_legend: bool = Field(default=True)
    connect_null_points: bool = Field(default=False)
    background_color: Color = Field(default="#FFFFFF")
    interpolation: Literal["linear", "smooth"] = Field(default="linear")
    stacked: bool = Field(default=False)

class LineChart(LineChartMetadata):
    data: List[List[Union[DateType, float]]] = Field(
        ...,
        min_items=1,
        description="List of points, where each point is [date, value1, value2, ...]"
    )