from typing import Union, Optional, Callable, Tuple, Any, List, Dict
from pydantic import BaseModel
from enum import Enum
from beanie import Document

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


# search
class RLGradSchema(BaseModel):
    lrs: List[float]
    distance_penalty: Optional[float]
    max_norm: Optional[float]
    norm_type: Union[float, int, str, None]

class TopKUpdateTypes(str, Enum):
    continuous = 'continuous'
    discrete = 'discrete'

class SearchRequest(BaseModel):
    data_source: str 
    filter: Optional[str]
    score: str 
    prune: Optional[TopKPruneSchema]
    iterations: int 
    initial_embeddings: List[List[float]]

class TopKSearchRequest(SearchRequest):
    grad_query: Optional[RLGradSchema] 
    update_k: int
    update_type: TopKUpdateTypes = TopKUpdateTypes.continuous

class RLSearchRequest(SearchRequest):
    rl_update: RLGradSchema

class SearchDocument(Document):
    search_request: Union[RLSearchRequest, TopKSearchRequest]
    batch_log: Optional[List]
    results: Optional[List]

