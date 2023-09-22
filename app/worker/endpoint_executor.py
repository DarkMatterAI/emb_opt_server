from emb_opt.imports import *
from emb_opt.executor import Executor
from ..schemas import EndpointDocument, InvokeItem, EndpointTypesResponse

class EndpointExecutor(Executor):
    def __init__(self, endpoint_document: EndpointDocument):
        self.endpoint_document = endpoint_document
        self.endpoint_type = self.endpoint_document.endpoint_type
        self.url = self.endpoint_document.endpoint_data.url
        self.batched = True 
        self.batch_size = self.endpoint_document.endpoint_data.batch_size
        self.concurrency = self.endpoint_document.endpoint_data.concurrency
        self.required_fields = set([k for k,v in 
                    self.endpoint_document.required_fields.model_dump().items() if v])

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
        response = [EndpointTypesResponse[self.endpoint_type](**i) for i in response]
        return response

    @classmethod
    async def from_id(cls, endpoint_id):
        endpoint_document = await schemas.EndpointDocument.get(endpoint_id)
        return cls(endpoint_document)
