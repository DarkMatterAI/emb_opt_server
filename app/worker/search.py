import os 
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie

from emb_opt.imports import * 
from emb_opt.utils import build_batch_from_embeddings
from emb_opt.prune import TopKPrune
from emb_opt.data_source import DataPluginGradWrapper
from emb_opt.update import (
                            RLUpdate, 
                            TopKContinuousUpdate, 
                            TopKDiscreteUpdate, 
                            UpdatePluginGradientWrapper
                            )
from emb_opt.runner import Runner 
                            
from .endpoint_executor import EndpointExecutor
from ..schemas import SearchDocument, EndpointDocument, SearchRequest

async def load_endpoints(search_request: SearchRequest):
    data_plugin = await EndpointExecutor.from_id(search_request.data_source_id, internal=True)
    filter_plugin = await EndpointExecutor.from_id(search_request.filter_id, internal=True)
    score_plugin = await EndpointExecutor.from_id(search_request.score_id, internal=True)

    return data_plugin, filter_plugin, score_plugin 

def load_prune_plugin(search_request):
    prune_plugin = None 
    if search_request.prune_schema is not None:
        prune_plugin = TopKPrune(search_request.prune_schema.k,
                                search_request.prune_schema.score_agg,
                                search_request.prune_schema.group_by)

    return prune_plugin

def load_rl_update(search_request):
    update_schema = search_request.update_schema
    update_plugin = RLUpdate(update_schema.lrs,
                            update_schema.distance_penalty,
                            update_schema.max_norm,
                            update_schema.norm_type
                            )
    return update_plugin

def load_topk_update(search_request, data_plugin):
    update_schema = search_request.update_schema
    if update_schema.update_type=='continuous':
        update_plugin = TopKContinuousUpdate(update_schema.update_k)
    else:
        update_plugin = TopKDiscreteUpdate(update_schema.update_k)

    if search_request.grad_query is not None:
        update_plugin = UpdatePluginGradientWrapper(update_plugin,
                                                    search_request.grad_query.distance_penalty,
                                                    search_request.grad_query.max_norm,
                                                    search_request.grad_query.norm_type
                                                    )
        data_plugin = DataPluginGradWrapper(data_plugin, search_request.grad_query.lrs)

    return update_plugin, data_plugin

async def load_plugins(search_document: SearchDocument):
    data_plugin, filter_plugin, score_plugin = await load_endpoints(search_document.search_request)

    prune_plugin = load_prune_plugin(search_document.search_request)

    if search_document.search_data.search_type == 'topk':
        update_plugin, data_plugin = load_topk_update(search_document.search_request, data_plugin)
    elif search_document.search_data.search_type == 'rl':
        update_plugin = load_rl_update(search_document.search_request) 

    plugin_dict = {}
    plugin_dict['data_plugin'] = data_plugin
    plugin_dict['filter_plugin'] = filter_plugin
    plugin_dict['score_plugin'] = score_plugin
    plugin_dict['prune_plugin'] = prune_plugin 
    plugin_dict['update_plugin'] = update_plugin

    return plugin_dict

def convert_floats(item):
    if type(item)==list:
        item = [convert_floats(i) for i in item]
    elif type(item)==dict:
        item = {k:convert_floats(v) for k,v in item.items()}
    elif type(item)==np.float32:
        item = float(item)
    elif type(item) == np.ndarray:
        item = item.tolist()
        
    return item

async def run_search(search_request_id: str):
    client = AsyncIOMotorClient(os.environ.get("MONGO_URI", None))
    await init_beanie(database=client[os.environ.get("MONGO_DB_NAME", None)], 
                      document_models=[SearchDocument, EndpointDocument])

    search_document = await SearchDocument.get(search_request_id)
    plugin_dict = await load_plugins(search_document)
    
    runner = Runner(**plugin_dict)

    batch = build_batch_from_embeddings(search_document.search_request.initial_embeddings)

    _, log = runner.search(batch, search_document.search_request.iterations, verbose=False)

    batch_log = convert_floats(log.dump_batch_log())['batch_log']
    results = convert_floats(log.compile_results())

    await search_document.set({SearchDocument.batch_log : batch_log,
                                SearchDocument.results : results})

    print('finished')
    return True 

