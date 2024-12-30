from enum import Enum
from pydantic import BaseModel, Field, field_validator
from typing import List, Literal, Optional, Union
from .misc import Color
from .base import BaseChart, ChartType

class BarPattern(str, Enum):
    SOLID = "solid"
    STRIPES = "stripes"
    DOTS = "dots"
    CROSSHATCH = "crosshatch"
    DIAGONAL = "diagonal"
    ZIGZAG = "zigzag"

class DatasetConfig(BaseModel):
    label: str = Field(..., min_length=1, max_length=50, description="Label for this dataset")
    color: Union[Color, List[Color]] = Field(default="#000000", description="Single color or array of colors for individual bars")
    pattern: Optional[BarPattern] = Field(None, description="Fill pattern for bars")

    @field_validator('color')
    def validate_colors_length(cls, v, values, **kwargs):
        if isinstance(v, list) and 'parent_data' in kwargs['field_info'].extra:
            data_length = len(kwargs['field_info'].extra['parent_data'])
            if len(v) != data_length:
                raise ValueError(f"Colors array length ({len(v)}) must match dataset length ({data_length})")
        return v

class AxisConfig(BaseModel):
    label: str = Field(..., min_length=1, max_length=50)
    show_grid: bool = Field(default=True)
    show_line: bool = Field(default=True)

class YAxisConfig(AxisConfig):
    min: Optional[float] = None
    max: Optional[float] = None
    log_scale: bool = Field(default=False)

class BarChartMetadata(BaseChart):
    type: Literal[ChartType.BAR]
    dataset_configs: List[DatasetConfig] = Field(..., min_items=1, max_items=10)
    x_axis: AxisConfig
    y_axis: YAxisConfig
    show_legend: bool = Field(default=True)
    background_color: Color = Field(default="#FFFFFF")
    bar_width: float = Field(default=0.8, ge=0.1, le=1.0)
    stack_mode: Literal["none", "stack", "stack_100"] = Field(default="none")
    horizontal: bool = Field(default=False)
    rounded_corners: bool = Field(default=False)

class BarChart(BarChartMetadata):
    data: List[List[Union[str, float]]] = Field(
        ...,
        min_items=1,
        description="List of points, where each point is [category, value1, value2, ...]"
    )