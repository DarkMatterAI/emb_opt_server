from fastapi import APIRouter, responses
from .. import crud 
from ..docs import DATA_SOURCE_DOCS
from ..schemas import schemas_crud 

router = APIRouter(default_response_class=responses.ORJSONResponse)

@router.get("/docs")
def get_docs():
    return DATA_SOURCE_DOCS

@router.post("/create", response_model=schemas_crud.EndpointDocument)
async def create_api(endpoint_schema: schemas_crud.CreateQueryEndpoint):
    item = await crud.create_endpoint(endpoint_schema, 'data_source')
    return item  

@router.get("/get/{endpoint_id}", response_model=schemas_crud.EndpointDocument)
async def get_api(endpoint_id: str):
    item = await crud.get_endpoint(endpoint_id)
    return item 

@router.post("/update/{endpoint_id}", response_model=schemas_crud.EndpointDocument)
async def create_api(endpoint_id: str, endpoint_schema: schemas_crud.CreateQueryEndpoint):
    item = await crud.update_endpoint(endpoint_id, endpoint_schema, 'data_source')
    return item  

@router.delete("/delete/{endpoint_id}")
async def delete_api(endpoint_id: str):
    item = await crud.delete_endpoint(endpoint_id)
    return item 

@router.get("/scroll", response_model=list[schemas_crud.EndpointDocument])
async def scroll_api(skip: int=0, limit: int=100):
    items = await crud.scroll_assembly_schema(skip, limit, 'data_source')
    return items 

