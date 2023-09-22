from fastapi import APIRouter, responses
from .. import schemas, crud 

router = APIRouter(default_response_class=responses.ORJSONResponse)

@router.get("/docs/{endpoint_type}")
def docs_api(endpoint_type: schemas.EndpointTypes):
    return crud.get_endpoint_docs(endpoint_type)

@router.post("/create_endpoint", response_model=schemas.EndpointDocument)
async def create_api(endpoint_data: schemas.CreateEndpoint):
    item = await crud.create_endpoint(endpoint_data)
    return item  

@router.get("/get/{endpoint_id}", response_model=schemas.EndpointDocument)
async def get_api(endpoint_id: str):
    item = await crud.get_endpoint(endpoint_id)
    return item 

@router.post("/update/{endpoint_id}", response_model=schemas.EndpointDocument)
async def create_api(endpoint_id: str, endpoint_data: schemas.CreateEndpoint):
    item = await crud.update_endpoint(endpoint_id, endpoint_data)
    return item  

@router.delete("/delete/{endpoint_id}")
async def delete_api(endpoint_id: str):
    item = await crud.delete_endpoint(endpoint_id)
    return item 

@router.get("/scroll", response_model=list[schemas.EndpointDocument])
async def scroll_api(skip: int=0, limit: int=100):
    items = await crud.scroll_endpoints(skip, limit)
    return items 

@router.get("/scroll/{endpoint_type}", response_model=list[schemas.EndpointDocument])
async def scroll_api(endpoint_type: schemas.EndpointTypes, skip: int=0, limit: int=100):
    items = await crud.scroll_endpoints(skip, limit, endpoint_type=endpoint_type)
    return items 

@router.get("/scroll_by_name", response_model=list[schemas.EndpointDocument])
async def scroll_api(endpoint_name: str, skip: int=0, limit: int=100):
    items = await crud.scroll_endpoints(skip, limit, endpoint_name=endpoint_name)
    return items 

@router.post("/invoke/{endpoint_id}")
async def invoke_api(endpoint_id: str, invoke_data: list[schemas.InvokeItem]):
    results = await crud.invoke_endpoint(endpoint_id, invoke_data)
    return results   
