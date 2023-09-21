import os
from fastapi import HTTPException
from typing import Optional

from .. import schemas 
from .docs import DOCS_MAPPING 
from ..worker.endpoint_executor import EndpointExecutor

def get_endpoint_docs(endpoint_type: schemas.EndpointTypes):
    return DOCS_MAPPING[endpoint_type]

def check_endpoint_data(endpoint_data: dict):
    if endpoint_data['endpoint_data']['concurrency'] <= 0:
        raise HTTPException(status_code=403, detail=f"endpoint concurrency must be at least 1")

    if endpoint_data['endpoint_data']['batch_size'] <= 0:
        raise HTTPException(status_code=403, detail=f"endpoint batch size must be at least 1")

    if not any([v for v in endpoint_data['required_fields'].values()]):
        raise HTTPException(status_code=403, detail=f"At least one request field must be True")


async def create_endpoint(endpoint_data: schemas.CreateEndpoint):

    endpoint_data = endpoint_data.model_dump()
    check_endpoint_data(endpoint_data)

    new_item = schemas.EndpointDocument(**endpoint_data)
    new_item = await new_item.insert()
    return new_item 

async def get_endpoint(endpoint_id: str):
    item = await schemas.EndpointDocument.get(endpoint_id)

    if item is None:
        raise HTTPException(status_code=404, detail=f"endpoint {endpoint_id} not found")

    return item

async def update_endpoint(endpoint_id: str, endpoint_data: schemas.CreateEndpoint):

    item = await get_endpoint(endpoint_id)

    endpoint_data = endpoint_data.model_dump()
    check_endpoint_data(endpoint_data)

    await item.set(endpoint_data)
    return item 

async def delete_endpoint(endpoint_id: str):
    item = await get_endpoint(endpoint_id)
    item = await item.delete()
    return {'success' : item.acknowledged}

async def scroll_endpoints(skip: int, 
                            limit: int, 
                            endpoint_type: Optional[schemas.EndpointTypes]=None,
                            endpoint_name: Optional[str]=None
                            ):

    if endpoint_type is not None:
        items = await schemas.EndpointDocument.find(
                                    schemas.EndpointDocument.endpoint_type==endpoint_type
                                                    ).skip(skip).limit(limit).to_list()
    elif endpoint_name is not None:
        items = await schemas.EndpointDocument.find(
                                    schemas.EndpointDocument.endpoint_data.name==endpoint_name
                                                    ).skip(skip).limit(limit).to_list()
    else:
        items = await schemas.EndpointDocument.find().skip(skip).limit(limit).to_list()
    return items 


async def invoke_endpoint(endpoint_id: str, invoke_data: list[schemas.InvokeItem]):
    endpoint = await get_endpoint(endpoint_id)
    executor = EndpointExecutor(endpoint)
    results = executor(invoke_data)
    return results 

