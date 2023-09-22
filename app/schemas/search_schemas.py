from typing import Union, Optional, Callable, Tuple, Any, List, Dict
from pydantic import BaseModel, Field, field_validator, model_validator
from enum import Enum

# prune
class TopKPruneAggTypes(str, Enum):
    mean = 'mean'
    max = 'max'

class TopKPruneGroup(str, Enum):
    collection_id = 'collection_id'
    parent_id = 'parent_id'

class TopKPruneSchema(BaseModel):
    k: int 
    score_agg: TopKPruneAggTypes = TopKPruneAggTypes.mean 
    group_by: Optional[TopKPruneGroup] 
        
    @field_validator('k')
    @classmethod
    def k_greater_than_zero(cls, k: int) -> int:
        if k <= 0:
            raise ValueError('k must be greater than 0')
        return k


# search
class RLGradSchema(BaseModel):
    lrs: List[float]
    distance_penalty: Optional[float]
    max_norm: Optional[float]
    norm_type: Union[float, int, str, None]
        
    @field_validator('lrs')
    @classmethod
    def valid_lrs(cls, lrs: List[float]) -> List[float]:
        if len(lrs) == 0:
            raise ValueError('must be at least one learning rate')
            
        for lr in lrs:
            if lr <= 0.0:
                raise ValueError('learning rate must be positive nonzero')
                
        return lrs

    @field_validator('distance_penalty')
    @classmethod
    def distance_penalty(cls, distance_penalty: Optional[float]) -> float:
        if distance_penalty is None:
            distance_penalty = 0

        return distance_penalty
    
    @model_validator(mode='after')
    def validate_norm(self):
        valid_norms = set(['inf', '-inf', 'fro', 'nuc'])
        
        if ((self.max_norm is None) and (self.norm_type is not None) or 
           (self.max_norm is not None) and (self.norm_type is None)):
            raise ValueError('to clip gradients, both max_norm and norm_type must be specified')
            
        if type(self.norm_type)==str:
            if not (self.norm_type in valid_norms):
                raise ValueError(f'norm must be nonzero int or one of {valid_norms}')
                        
        return self

class TopKUpdateTypes(str, Enum):
    continuous = 'continuous'
    discrete = 'discrete'

class TopKUpdateSchema(BaseModel):
    update_k: int
    update_type: TopKUpdateTypes = TopKUpdateTypes.continuous
        
    @field_validator('update_k')
    @classmethod
    def update_k_greater_than_zero(cls, update_k: int) -> int:
        if update_k <= 0:
            raise ValueError('update_k must be greater than 0')
        return update_k

class SearchRequest(BaseModel):
    data_source_id: str 
    filter_id: Optional[str]
    score_id: str 
    prune_schema: Optional[TopKPruneSchema]
    update_schema: None
    iterations: int 
    initial_embeddings: List[List[float]]
        
    @field_validator('iterations')
    @classmethod
    def iteration_greater_than_zero(cls, iterations: int) -> int:
        if iterations <= 0:
            raise ValueError('iterations must be greater than 0')
        return iterations
    
    @field_validator('initial_embeddings')
    @classmethod
    def num_initial_embeddings(cls, initial_embeddings: List[List[float]]) -> List[List[float]]:
        if len(initial_embeddings) == 0:
            raise ValueError('must be at least one initial embedding')
        return initial_embeddings

class TopKSearchRequest(SearchRequest):
    grad_query: Optional[RLGradSchema] 
    update_schema: TopKUpdateSchema

class RLSearchRequest(SearchRequest):
    update_schema: RLGradSchema
    # rl_update: RLGradSchema

class SearchTypes(str, Enum):
    topk = 'topk'
    rl = 'rl'

class SearchData(BaseModel):
    search_type: SearchTypes = SearchTypes.topk
    status: Optional[str]
    num_results: Optional[int]

class SearchResponse(BaseModel):
    id: str = Field(..., alias='_id')
    search_data: SearchData
