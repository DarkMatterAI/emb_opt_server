from emb_opt.imports import *
from emb_opt.utils import build_batch_from_embeddings
from emb_opt.executor import Executor
from emb_opt.prune import TopKPrune
from emb_opt.data_source import DataPluginGradWrapper
from emb_opt.update import (
                            UpdatePluginGradientWrapper, 
                            TopKDiscreteUpdate,
                            TopKContinuousUpdate,
                            RLUpdate
                            )
from emb_opt.runner import Runner 

class APIExecutor(Executor):
    def __init__(self,
                 url: str,                     # API URL
                 batched: bool,                # if inputs should be batched
                 batch_size: int=1,            # batch size (set batch_size=0 to pass all inputs)
                 concurrency: Optional[int]=1  # number of concurrent threads
                ):
        
        self.url = url
        self.batched = batched
        self.concurrency = concurrency
        self.batch_size = batch_size
        
    def function(self, inputs: List[BaseModel]):
        response = requests.post(self.url, json=inputs)
        return response.json()
        
    def execute(self, inputs: List[BaseModel]):
        if (self.concurrency is None) or (self.concurrency==1):
            results = [self.function(i) for i in inputs]
        else:
            with ThreadPoolExecutor(min(self.concurrency, len(inputs))) as p:
                results = list(p.map(self.function, inputs))
            
        return results

class EndpointExecutor(APIExecutor):
    def __init__(self, endpoint_data, request_data):
        self.url = endpoint_data['url']
        self.batched = True
        self.concurrency = endpoint_data['concurrency']
        self.batch_size = endpoint_data['batch_size']
        self.request_data = request_data

    def function(self, inputs: List[BaseModel]):
        request_inputs = []
        for item in inputs:
            item = item.model_dump()
            item = {k:item[k] if self.request_data[k] else None for k in self.request_data.keys()}
            request_inputs.append(item)
        
        response = requests.post(self.url, json=request_inputs)
        return response.json()

    @classmethod
    def from_endpoint_data(cls, endpoint_data):
        return cls(endpoint_data['endpoint_data'], endpoint_data['request_data'])


def topk_search(search_schema):

    print('building plugins')
    data_plugin = EndpointExecutor.from_endpoint_data(search_schema['data_source'])
    filter_plugin = EndpointExecutor.from_endpoint_data(search_schema['filter'])
    score_plugin = EndpointExecutor.from_endpoint_data(search_schema['score'])

    prune_plugin = None
    if search_schema['prune']:
        prune_plugin = TopKPrune(search_schema['prune']['k'],
                                search_schema['prune']['score_agg'],
                                search_schema['prune']['group_by'])

    if search_schema['update_type'] == 'continuous':
        update_plugin = TopKContinuousUpdate(search_schema['update_k'])
    else:
        update_plugin = TopKDiscreteUpdate(search_schema['update_k'])

    if search_schema['grad_query'] is not None:
        data_plugin = DataPluginGradWrapper(data_plugin, search_schema['grad_query']['lrs'])
        update_plugin = UpdatePluginGradientWrapper(update_plugin, 
                                                    search_schema['grad_query']['distance_penalty'],
                                                    search_schema['grad_query']['max_norm'],
                                                    search_schema['grad_query']['norm_type']
                                                    )

    print('building runner')
    runner = Runner(data_plugin, filter_plugin, score_plugin, prune_plugin, update_plugin)

    print('creating batch')
    batch = build_batch_from_embeddings(search_schema['initial_embeddings'])

    print('running')
    _, log = runner.search(batch, search_schema['iterations'])

    print('finished')

    


