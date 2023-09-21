from typing import Optional, Union
from motor.motor_asyncio import AsyncIOMotorClient
from fastapi import HTTPException

from .schemas import schemas_crud, schemas_search
from .config import CONFIG

if CONFIG.MONGO_URI:
    client = AsyncIOMotorClient(CONFIG.MONGO_URI)
else:
    client = None

from .worker.search_runner import topk_search

def check_endpoint_data(endpoint_data: dict):
    if endpoint_data['endpoint_data']['concurrency'] <= 0:
        raise HTTPException(status_code=403, detail=f"endpoint concurrency must be at least 1")

    if endpoint_data['endpoint_data']['batch_size'] <= 0:
        raise HTTPException(status_code=403, detail=f"endpoint batch soze must be at least 1")

async def create_endpoint(
                endpoint_schema: Union[schemas_crud.CreateQueryEndpoint, schemas_crud.CreateItemEndpoint],
                endpoint_type: str
                ):
    endpoint_data = endpoint_schema.model_dump()
    endpoint_data['endpoint_type'] = endpoint_type

    check_endpoint_data(endpoint_data)

    new_item = schemas_crud.EndpointDocument(**endpoint_data)
    new_item = await new_item.insert()
    return new_item 

async def get_endpoint(endpoint_id: str):
    item = await schemas_crud.EndpointDocument.get(endpoint_id)

    if item is None:
        raise HTTPException(status_code=404, detail=f"endpoint {endpoint_id} not found")

    return item

async def delete_endpoint(endpoint_id: str):
    item = await get_endpoint(endpoint_id)
    item = await item.delete()
    return {'success' : item.acknowledged}


async def scroll_assembly_schema(skip: int, 
                                limit: int, 
                                endpoint_type: Optional[schemas_crud.EndpointTypes]=None):

    if endpoint_type is not None:
        items = await schemas_crud.EndpointDocument.find(
                                    schemas_crud.EndpointDocument.endpoint_type==endpoint_type
                                                    ).skip(skip).limit(limit).to_list()
    else:
        items = await schemas_crud.EndpointDocument.find().skip(skip).limit(limit).to_list()
    return items 

async def update_endpoint(
                endpoint_id: str,
                endpoint_schema: Union[schemas_crud.CreateQueryEndpoint, schemas_crud.CreateItemEndpoint],
                endpoint_type: str
                ):

    item = await get_endpoint(endpoint_id)

    endpoint_data = endpoint_schema.model_dump()
    endpoint_data['endpoint_type'] = endpoint_type

    check_endpoint_data(endpoint_data)

    await item.set(endpoint_data)
    return item 


async def create_topk_search(search_request: schemas_search.TopKSearchRequest):
    data_endpoint = await get_endpoint(search_request.data_source)

    filter_endpoint = None 
    if search_request.filter is not None:
        filter_endpoint = await get_endpoint(search_request.filter)

    score_endpoint = await get_endpoint(search_request.score)

    prune_schema = search_request.prune 

    if data_endpoint.request_data.item:
        if search_request.grad_query is not None:
            raise HTTPException(status_code=403, detail=f"data endpoint incompatible with grad query")

        if update_type=='continuous':
            raise HTTPException(status_code=403, detail=f"data endpoint incompatible with continuous update")

    search_schema = search_request.model_dump()
    search_schema['data_source'] = data_endpoint.model_dump()
    search_schema['filter'] = filter_endpoint.model_dump() if filter_endpoint else filter_endpoint
    search_schema['score'] = score_endpoint.model_dump()

    topk_search(search_schema)

    return search_schema


async def create_rl_search(search_request: schemas_search.RLSearchRequest):
    data_endpoint = await get_endpoint(search_request.data_source)

    filter_endpoint = None 
    if search_request.filter is not None:
        filter_endpoint = await get_endpoint(search_request.filter)

    score_endpoint = await get_endpoint(search_request.score)

    prune_schema = search_request.prune 

    if data_endpoint.request_data.item:
        raise HTTPException(status_code=403, detail=f"data endpoint incompatible with RL search")

    search_schema = search_request.model_dump()
    search_schema['data_source'] = data_endpoint.model_dump()
    search_schema['filter'] = filter_endpoint.model_dump() if filter_endpoint else filter_endpoint
    search_schema['score'] = score_endpoint.model_dump()

    return search_schema

