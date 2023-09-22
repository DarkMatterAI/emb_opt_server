import os
from fastapi import HTTPException
import asyncio

from .database_crud import get_endpoint
from .. import schemas 
from .. import worker

async def invoke_endpoint(endpoint_id: str, invoke_data: list[schemas.InvokeItem]):
    endpoint = await get_endpoint(endpoint_id)
    executor = worker.EndpointExecutor(endpoint)
    results = executor(invoke_data)

    return results 

async def validate_endpoint_and_type(endpoint_id, expected_type):
    endpoint = await get_endpoint(endpoint_id)
    if endpoint.endpoint_type != expected_type:
        raise HTTPException(status_code=400, 
                detail=f"expected endpoint of type {expected_type}, received {endpoint.endpoint_type}")

    return endpoint 

async def validate_search_schema(search_schema: schemas.SearchRequest, search_type: str):
    data_source_endpoint = await validate_endpoint_and_type(search_schema.data_source_id, 'data_source')
    filter_endpoint = await validate_endpoint_and_type(search_schema.filter_id, 'filter')
    score_endpoint = await validate_endpoint_and_type(search_schema.score_id, 'score')

    if search_type=='topk':
        if data_source_endpoint.required_fields.item==True:
            if search_schema.grad_query is not None:
                raise HTTPException(status_code=400, 
                        detail=f"data source requires item input, incompatible with grad query")

            if search_schema.update_schema.update_type=='continuous':
                raise HTTPException(status_code=400, 
                        detail=f"data source requires item input, incompatible with continuous update")

    elif search_type=='rl':
        if data_source_endpoint.required_fields.item==True:
            raise HTTPException(status_code=400, 
                    detail=f"data source requires item input, incompatible with rl search")

    return True 

async def create_topk_search(search_schema: schemas.TopKSearchRequest):
    await validate_search_schema(search_schema, 'topk')

    search_data = {'search_type':'topk', 'status':'received', 'num_results':0}
    new_search = schemas.SearchDocument(search_request=search_schema, batch_log=[], results=[],
                                        search_data=search_data)

    new_search = await new_search.insert()
    response = new_search.model_dump(include={'id', 'search_data'}, by_alias=True)
    celery_job = worker.create_search.apply_async(kwargs={'search_request_id':response['_id']}, queue='search_queue')

    return response 

async def create_rl_search(search_schema: schemas.TopKSearchRequest):
    # await validate_search_schema(search_schema, 'rl')

    # search_data = {'search_type':'rl', 'status':'received', 'num_results':0}
    # new_search = schemas.SearchDocument(search_request=search_schema, batch_log=[], results=[],
    #                                     search_data=search_data)

    return {'success' : True}

async def get_search(search_id: str, dump=True):
    item = await schemas.SearchDocument.get(search_id)

    if item is None:
        raise HTTPException(status_code=404, detail=f"search {search_id} not found")

    if dump:
        item = item.model_dump(include={'id', 'search_data'}, by_alias=True)

    return item

async def delete_search(search_id: str):
    item = await get_search(search_id, dump=False)
    item = await item.delete()
    return {'success' : item.acknowledged}

async def scroll_search(skip: int, limit: int):

    items = await schemas.SearchDocument.find().skip(skip).limit(limit).to_list()
    items = [item.model_dump(include={'id', 'search_data'}, by_alias=True) for item in items]

    return items 

