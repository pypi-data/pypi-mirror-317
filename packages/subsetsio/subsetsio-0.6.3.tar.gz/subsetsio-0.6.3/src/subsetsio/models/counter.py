from pydantic import BaseModel, Field, field_validator
from typing import List, Literal, Optional, Union
from .base import BaseChart, ChartType
from .misc import Color
from enum import Enum

class GradientStop(BaseModel):
    color: Color
    position: float = Field(ge=0, le=1, description="Position of the color stop (0-1)")
    opacity: float = Field(default=1.0, ge=0, le=1)

class GradientDirection(str, Enum):
    HORIZONTAL = "horizontal"
    VERTICAL = "vertical"
    DIAGONAL = "diagonal"
    RADIAL = "radial"

class BackgroundEffect(BaseModel):
    gradient_stops: List[GradientStop] = Field(min_items=2, max_items=5)
    direction: GradientDirection = Field(default=GradientDirection.VERTICAL)
    blur_radius: float = Field(default=0, ge=0, le=100, description="Blur effect radius in pixels")

class CounterChartMetadata(BaseChart):
    type: Literal[ChartType.COUNTER]
    text_color: Color = Field(default=Color("#000000"))
    background_color: Color = Field(default=Color("#FFFFFF"))
    background_effect: Optional[BackgroundEffect] = None
    prefix: Optional[str] = None
    postfix: Optional[str] = None
    value_color: Color = Field(default=Color("#000000"))
    prefix_color: Color = Field(default=Color("#000000"))
    postfix_color: Color = Field(default=Color("#000000"))

class CounterChart(CounterChartMetadata):
    value: float