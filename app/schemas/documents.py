from beanie import Document
from .crud_schemas import EndpointDataInternal, EndpointTypes, RequiredRequestFields

class EndpointDocument(Document):
    endpoint_data: EndpointDataInternal
    endpoint_type: EndpointTypes
    required_fields: RequiredRequestFields

DOCUMENT_MODELS = [EndpointDocument]