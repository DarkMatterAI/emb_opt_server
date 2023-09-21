from typing import Union, Optional, Callable, Tuple, Any, List, Dict
from pydantic import BaseModel, AnyHttpUrl, field_serializer
from enum import Enum

class EndpointData(BaseModel):
    name: Optional[str]
    url: AnyHttpUrl 
    concurrency: int 
    batch_size: int
        
    @field_serializer('url')
    def serialize_dt(self, url: AnyHttpUrl, _info):
        return str(url)

class EndpointDataInternal(BaseModel):
    name: Optional[str]
    url: str 
    concurrency: int 
    batch_size: int

class RequiredRequestFields(BaseModel):
    item: bool 
    embedding: bool
    data: bool

class EndpointTypes(str, Enum):
    data_source = 'data_source'
    filter = 'filter'
    score = 'score'

class CreateEndpoint(BaseModel):
    endpoint_data: EndpointData
    required_fields: RequiredRequestFields
    endpoint_type: EndpointTypes

