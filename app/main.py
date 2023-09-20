from fastapi import FastAPI, responses
from .database import init_mongodb

from . import schemas 
from . import crud 

app = FastAPI(default_response_class=responses.ORJSONResponse)

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.on_event("startup")
async def init_db():
    await init_mongodb()

@app.post("/create_data_source", response_model=schemas.common.EndpointDocument)
async def create_data_source_api(endpoint_schema: schemas.common.CreateQueryEndpoint):
    item = await crud.common.create_endpoint(endpoint_schema, 'data_source')
    return item  

@app.post("/create_filter", response_model=schemas.common.EndpointDocument)
async def create_filter_api(endpoint_schema: schemas.common.CreateItemEndpoint):
    item = await crud.common.create_endpoint(endpoint_schema, 'filter')
    return item  

@app.post("/create_score", response_model=schemas.common.EndpointDocument)
async def create_score_api(endpoint_schema: schemas.common.CreateItemEndpoint):
    item = await crud.common.create_endpoint(endpoint_schema, 'score')
    return item  

@app.post("/create_prune", response_model=schemas.common.EndpointDocument)
async def create_prune_api(endpoint_schema: schemas.common.CreateQueryEndpoint):
    item = await crud.common.create_endpoint(endpoint_schema, 'prune')
    return item  

@app.post("/create_update", response_model=schemas.common.EndpointDocument)
async def create_prune_api(endpoint_schema: schemas.common.CreateQueryEndpoint):
    item = await crud.common.create_endpoint(endpoint_schema, 'update')
    return item  

@app.get("/get_endpoint/{endpoint_id}", response_model=schemas.common.EndpointDocument)
async def get_endpoint_api(endpoint_id: str):
    item = await crud.common.get_endpoint(endpoint_id)
    return item 

@app.delete("/delete_endpoint/{endpoint_id}")
async def delete_endpoint_api(endpoint_id: str):
    item = await crud.common.delete_endpoint(endpoint_id)
    return item 

@app.get("/scroll_endpoints", response_model=list[schemas.common.EndpointDocument])
async def scroll_endpoints_api(skip: int=0, limit: int=100):
    items = await crud.common.scroll_assembly_schema(skip, limit)
    return items 

@app.get("/scroll_endpoints/{endpoint_type}", response_model=list[schemas.common.EndpointDocument])
async def scroll_endpoints_api(endpoint_type: schemas.common.EndpointTypes, skip: int=0, limit: int=100):
    items = await crud.common.scroll_assembly_schema(skip, limit, endpoint_type)
    return items 
