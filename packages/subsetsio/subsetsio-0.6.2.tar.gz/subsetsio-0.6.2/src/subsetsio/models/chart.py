from enum import Enum
from typing import Optional, Union
from .base import ChartType
from .bar import BarChart, BarChartMetadata
from .counter import CounterChart, CounterChartMetadata
from .line import LineChart, LineChartMetadata
from .map import MapChart, MapChartMetadata
from .scatter import ScatterplotChart, ScatterplotChartMetadata
from .table import TableChart, TableChartMetadata


Chart = Union[LineChart, MapChart, BarChart, CounterChart, ScatterplotChart, TableChart]
ChartMetadata = Union[LineChartMetadata, MapChartMetadata, BarChartMetadata, CounterChartMetadata, ScatterplotChartMetadata, TableChartMetadata]

def parse_chart(data: dict) -> Chart:
    chart_type = data.get('type')
    if chart_type == ChartType.LINE:
        return LineChart(**data)
    elif chart_type == ChartType.MAP:
        return MapChart(**data)
    elif chart_type == ChartType.BAR:
        return BarChart(**data)
    elif chart_type == ChartType.COUNTER:
        return CounterChart(**data)
    elif chart_type == ChartType.SCATTERPLOT:
        return ScatterplotChart(**data)
    elif chart_type == ChartType.TABLE:
        return TableChart(**data)
    else:
        raise ValueError(f"Unsupported chart type: {chart_type}")
    
def parse_chart_metadata(data: dict) -> ChartMetadata:
    chart_type = data.get('type')
    if chart_type == ChartType.LINE:
        return LineChartMetadata(**data)
    elif chart_type == ChartType.MAP:
        return MapChartMetadata(**data)
    elif chart_type == ChartType.BAR:
        return BarChartMetadata(**data)
    elif chart_type == ChartType.COUNTER:
        return CounterChartMetadata(**data)
    elif chart_type == ChartType.SCATTERPLOT:
        return ScatterplotChartMetadata(**data)
    elif chart_type == ChartType.TABLE:
        return TableChartMetadata(**data)
    else:
        raise ValueError(f"Unsupported chart type: {chart_type}")