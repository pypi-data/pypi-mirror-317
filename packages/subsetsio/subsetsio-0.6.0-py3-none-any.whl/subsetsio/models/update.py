from typing import TypeVar, Union, Type, get_args
from pydantic import BaseModel, create_model, ConfigDict, model_validator
from .chart import (
    BarChartMetadata, LineChartMetadata, MapChartMetadata,
    CounterChartMetadata, ScatterplotChartMetadata, TableChartMetadata
)

def make_optional(model: Type[BaseModel]) -> Type[BaseModel]:
    """Makes all fields except 'type' optional and excluded from the model"""
    fields = {}
    for name, field in model.model_fields.items():
        if name != 'type':  # Skip the type field entirely
            field_info = field.annotation
            fields[name] = (Union[field_info, None], None)
    
    class UpdateModelBase(BaseModel):
        model_config = ConfigDict(extra='forbid')  # This is key - it will reject unknown fields
        
        @model_validator(mode='after')
        def validate_update(self):
            update_fields = {
                k: v for k, v in self.__dict__.items() 
                if v is not None
            }
            if not update_fields:
                raise ValueError("At least one field must be provided for update")
            return self

    model_cls = create_model(
        f'{model.__name__}Update',
        __base__=UpdateModelBase,
        **fields
    )

    return model_cls

# Create update models for each chart type's metadata using make_optional
BarChartMetadataUpdate = make_optional(BarChartMetadata)
LineChartMetadataUpdate = make_optional(LineChartMetadata)
MapChartMetadataUpdate = make_optional(MapChartMetadata)
CounterChartMetadataUpdate = make_optional(CounterChartMetadata)
ScatterplotChartMetadataUpdate = make_optional(ScatterplotChartMetadata)
TableChartMetadataUpdate = make_optional(TableChartMetadata)

# Map chart types to their update models
UPDATE_MODEL_MAP = {
    'bar': BarChartMetadataUpdate,
    'line': LineChartMetadataUpdate,
    'map': MapChartMetadataUpdate,
    'counter': CounterChartMetadataUpdate,
    'scatter': ScatterplotChartMetadataUpdate,
    'table': TableChartMetadataUpdate
}

# Union of all chart metadata update types
ChartUpdate = Union[
    BarChartMetadataUpdate,
    LineChartMetadataUpdate,
    MapChartMetadataUpdate,
    CounterChartMetadataUpdate,
    ScatterplotChartMetadataUpdate,
    TableChartMetadataUpdate
]