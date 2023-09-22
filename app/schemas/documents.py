from typing import Union, List, Optional
from beanie import Document
from .crud_schemas import EndpointDataInternal, EndpointTypes, RequiredRequestFields
from .search_schemas import RLSearchRequest, TopKSearchRequest, SearchData

class EndpointDocument(Document):
    endpoint_data: EndpointDataInternal
    endpoint_type: EndpointTypes
    required_fields: RequiredRequestFields

class SearchDocument(Document):
    search_request: Union[RLSearchRequest, TopKSearchRequest]
    batch_log: Optional[List]
    results: Optional[List]
    search_data: Optional[SearchData]

DOCUMENT_MODELS = [EndpointDocument, SearchDocument]
