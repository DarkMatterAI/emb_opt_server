from typing import Union, Optional, Callable, Tuple, Any, List, Dict
from enum import Enum
from pydantic import (
                    BaseModel, 
                    AnyHttpUrl, 
                    field_serializer, 
                    field_validator, 
                    model_validator, 
                    FieldValidationInfo
                    )

class EndpointData(BaseModel):
    name: Optional[str]
    url: AnyHttpUrl 
    concurrency: int 
    batch_size: int
        
    @field_serializer('url')
    def serialize_dt(self, url: AnyHttpUrl, _info):
        return str(url)

    @field_validator('concurrency', 'batch_size')
    @classmethod
    def check_greater_than_zero(cls, v: int, info: FieldValidationInfo) -> int:
        if v<=0:
            raise ValueError(f'{info.field_name} must be greater than zero')
        return v

class EndpointDataInternal(BaseModel):
    name: Optional[str]
    url: str 
    concurrency: int 
    batch_size: int

    @field_validator('concurrency', 'batch_size')
    @classmethod
    def check_greater_than_zero(cls, v: int, info: FieldValidationInfo) -> int:
        if v<=0:
            raise ValueError(f'{info.field_name} must be greater than zero')
        return v

class RequiredRequestFields(BaseModel):
    item: bool 
    embedding: bool
    data: bool

    @model_validator(mode='after')
    def validate_inputs(self):
        
        if not any([self.item, self.embedding, self.data]):
            raise ValueError(f'at least one of [item, embedding, data] must be True')
                        
        return self

class EndpointTypes(str, Enum):
    data_source = 'data_source'
    filter = 'filter'
    score = 'score'

class CreateEndpoint(BaseModel):
    endpoint_data: EndpointData
    required_fields: RequiredRequestFields
    endpoint_type: EndpointTypes

