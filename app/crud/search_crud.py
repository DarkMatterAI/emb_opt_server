import os
from fastapi import HTTPException
import asyncio

from .database_crud import get_endpoint
from .. import schemas 
from ..worker.endpoint_executor import EndpointExecutor

async def invoke_endpoint(endpoint_id: str, invoke_data: list[schemas.InvokeItem]):
    endpoint = await get_endpoint(endpoint_id)
    executor = EndpointExecutor(endpoint)
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

            if search_schema.update_type=='continuous':
                raise HTTPException(status_code=400, 
                        detail=f"data source requires item input, incompatible with continuous update")

    elif search_type=='rl':
        if data_source_endpoint.required_fields.item==True:
            raise HTTPException(status_code=400, 
                    detail=f"data source requires item input, incompatible with rl search")

    return True 

async def create_topk_search(search_schema: schemas.TopKSearchRequest):
    await validate_search_schema(search_schema, 'topk')
    return {'success' : True}

async def create_rl_search(search_schema: schemas.TopKSearchRequest):
    await validate_search_schema(search_schema, 'rl')
    return {'success' : True}

# test validation conditions
