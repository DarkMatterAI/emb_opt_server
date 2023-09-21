from pydantic import BaseModel
from typing import Optional, Union, List, Dict

class QueryRequest(BaseModel):
    item: Optional[str]
    embedding: Optional[List[float]]

class ItemRequest(BaseModel):
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