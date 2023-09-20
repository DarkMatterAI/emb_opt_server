from typing import Union, Optional, Callable, Tuple, Any, List, Dict
from pydantic import BaseModel, AnyHttpUrl, field_serializer
from beanie import Document
from enum import Enum

class EndpointData(BaseModel):
    url: AnyHttpUrl 
    concurrency: int 
    batch_size: int
        
    @field_serializer('url')
    def serialize_dt(self, url: AnyHttpUrl, _info):
        return str(url)

class EndpointDataInternal(BaseModel):
    url: str 
    concurrency: int 
    batch_size: int

class RequiredQueryFields(BaseModel):
    id: bool
    item: bool 
    embedding: bool
    data: bool
    query_results: bool
    internal: bool

class RequiredItemFields(BaseModel):
    id: bool
    item: bool 
    embedding: bool
    score: bool
    data: bool
    internal: bool

class EndpointTypes(str, Enum):
    data_source = 'data_source'
    filter = 'filter'
    score = 'score'
    prune = 'prune'
    update = 'update'

class EndpointDocument(Document):
    name: Optional[str]
    endpoint_type: EndpointTypes
    endpoint_data: EndpointDataInternal
    request_data: Union[RequiredQueryFields, RequiredItemFields]

class CreateQueryEndpoint(BaseModel):
    name: Optional[str]
    endpoint_data: EndpointData
    request_data: RequiredQueryFields

class CreateItemEndpoint(BaseModel):
    name: Optional[str]
    endpoint_data: EndpointData
    request_data: RequiredItemFields

