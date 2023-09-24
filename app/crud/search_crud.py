import os
from fastapi import HTTPException
import asyncio
from bson import ObjectId

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

async def create_search(search_schema: schemas.SearchRequest, search_type: str):
    await validate_search_schema(search_schema, search_type)

    search_data = {'search_type':search_type, 'status':'received', 'num_results':0}
    new_search = schemas.SearchDocument(search_request=search_schema, batch_log=[], results=[],
                                        search_data=search_data)

    new_search = await new_search.insert()
    response = new_search.model_dump(include={'id', 'search_data'}, by_alias=True)
    celery_job = worker.create_search.apply_async(kwargs={'search_request_id':response['_id']}, queue='search_queue')

    return response 

async def create_topk_search(search_schema: schemas.TopKSearchRequest):
    response = await create_search(search_schema, 'topk')
    return response 

async def create_rl_search(search_schema: schemas.TopKSearchRequest):
    response = await create_search(search_schema, 'rl')
    return response 

async def get_search(search_id: str, include_request: bool=True):
    motor_collection = schemas.SearchDocument.get_motor_collection()
    filter_dict = {'batch_log':0, 'results':0}
    if not include_request:
        filter_dict['search_request'] = 0
    
    document = await motor_collection.find_one(
        {"_id": ObjectId(search_id)},
        filter_dict
    )

    if document is None:
        raise HTTPException(status_code=404, detail=f"search {search_id} not found")

    return document

async def delete_search(search_id: str):
    motor_collection = schemas.SearchDocument.get_motor_collection()
    result = await motor_collection.delete_one({"_id": ObjectId(search_id)})
    return {'success' : result.acknowledged}

async def scroll_search(skip: int, limit: int, include_request: bool=True):
    filter_dict = {'batch_log':0, 'results':0}
    if not include_request:
        filter_dict['search_request'] = 0

    motor_collection = schemas.SearchDocument.get_motor_collection()
    documents = await motor_collection.find({}, filter_dict).skip(skip).limit(limit).to_list(limit)
    return documents

async def get_results(search_id: str, skip: int, limit: int):
    motor_collection = schemas.SearchDocument.get_motor_collection() 
    document = await motor_collection.find_one(
        {"_id": ObjectId(search_id)},
        {"results": {"$slice": [skip, limit]}, 
         "_id": 0, 'batch_log':0, 'search_request':0, 'search_data':0}
    )

    if document is None:
        raise HTTPException(status_code=404, detail=f"search {search_id} not found")

    return document['results']

async def get_batch_log(search_id: str, skip: int, limit: int):
    motor_collection = schemas.SearchDocument.get_motor_collection() 
    document = await motor_collection.find_one(
        {"_id": ObjectId(search_id)},
        {"batch_log": {"$slice": [skip, limit]}, 
         "_id": 0, 'results':0, 'search_request':0, 'search_data':0}
    )

    if document is None:
        raise HTTPException(status_code=404, detail=f"search {search_id} not found")

    return document['batch_log']



# do rl search proper    
# update num results in search
