from emb_opt.imports import *
from emb_opt.executor import Executor
from emb_opt.schemas import DataSourceResponse, FilterResponse, ScoreResponse

from ..schemas import EndpointDocument, InvokeItem, EndpointTypesResponse

EndpointTypesResponseInternal = {
    'data_source' : DataSourceResponse,
    'filter' : FilterResponse,
    'score' : ScoreResponse
}

class EndpointExecutor(Executor):
    def __init__(self, endpoint_document: EndpointDocument, internal=False):
        self.endpoint_document = endpoint_document
        self.endpoint_type = self.endpoint_document.endpoint_type
        self.url = self.endpoint_document.endpoint_data.url
        self.batched = True 
        self.batch_size = self.endpoint_document.endpoint_data.batch_size
        self.concurrency = self.endpoint_document.endpoint_data.concurrency
        self.required_fields = set([k for k,v in 
                    self.endpoint_document.required_fields.model_dump().items() if v])
        self.internal = internal 

    def execute(self, inputs: List[BaseModel]):
        if (self.concurrency is None) or (self.concurrency==1):
            results = [self.function(i) for i in inputs]
        else:
            with ThreadPoolExecutor(min(self.concurrency, len(inputs))) as p:
                results = list(p.map(self.function, inputs))
            
        return results

    def function(self, inputs: List[InvokeItem]):
        request_inputs = []
        for item in inputs:
            item = item.model_dump()
            request_item = {'item':None, 'embedding':None, 'data':None}

            for required_field in self.required_fields:
                request_item[required_field] = item[required_field]

            request_inputs.append(request_item)
        
        response = requests.post(self.url, json=request_inputs).json()

        if self.internal:
            response = [EndpointTypesResponseInternal[self.endpoint_type](**i) for i in response]
        else:
            response = [EndpointTypesResponse[self.endpoint_type](**i) for i in response]

        # response = [i.model_dump() for i in response]
        return response

    @classmethod
    async def from_id(cls, endpoint_id, internal=False):
        endpoint_document = await EndpointDocument.get(endpoint_id)
        return cls(endpoint_document, internal=internal)

