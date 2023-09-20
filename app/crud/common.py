from typing import Optional, Union
from motor.motor_asyncio import AsyncIOMotorClient
from fastapi import HTTPException

from .. import schemas
from ..config import CONFIG

if CONFIG.MONGO_URI:
    client = AsyncIOMotorClient(CONFIG.MONGO_URI)
else:
    client = None

async def create_endpoint(
                endpoint_schema: Union[schemas.common.CreateQueryEndpoint, schemas.common.CreateItemEndpoint],
                endpoint_type: str
                ):
    endpoint_data = endpoint_schema.model_dump()
    endpoint_data['endpoint_type'] = endpoint_type

    new_item = schemas.common.EndpointDocument(**endpoint_data)
    new_item = await new_item.insert()
    return new_item 

async def get_endpoint(endpoint_id: str):
    item = await schemas.common.EndpointDocument.get(endpoint_id)

    if item is None:
        raise HTTPException(status_code=404, detail=f"endpoint {endpoint_id} not found")

    return item

async def delete_endpoint(endpoint_id: str):
    item = await get_endpoint(endpoint_id)
    item = await item.delete()
    return {'success' : item.acknowledged}


async def scroll_assembly_schema(skip: int, 
                                limit: int, 
                                endpoint_type: Optional[schemas.common.EndpointTypes]=None):

    if endpoint_type is not None:
        items = await schemas.common.EndpointDocument.find(
                                    schemas.common.EndpointDocument.endpoint_type==endpoint_type
                                                    ).skip(skip).limit(limit).to_list()
    else:
        items = await schemas.common.EndpointDocument.find().skip(skip).limit(limit).to_list()
    return items 
