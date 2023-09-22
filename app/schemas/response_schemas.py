from typing import Optional, List, Union, Dict
from pydantic import BaseModel

class InvokeItem(BaseModel):
    item: Optional[str]
    embedding: Optional[List[float]]
    data: Optional[dict]

class ItemResponse(BaseModel):
    id: Optional[Union[str, int]]
    item: Optional[str]
    embedding: List[float]
    score: Optional[float]
    data: Optional[dict]

class DataSourceResponse(BaseModel):
    valid: bool
    data: Optional[Dict]
    query_results: List[ItemResponse]

class FilterResponse(BaseModel):
    valid: bool
    data: Optional[Dict]

class ScoreResponse(BaseModel):
    valid: bool
    score: Optional[float]
    data: Optional[Dict]

EndpointTypesResponse = {
    'data_source' : DataSourceResponse,
    'filter' : FilterResponse,
    'score' : ScoreResponse
}

