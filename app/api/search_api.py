from fastapi import APIRouter, responses
from .. import schemas, crud 

router = APIRouter(default_response_class=responses.ORJSONResponse)

@router.post("/create_topk_search", response_model=schemas.SearchResponse)
async def create_topk_search_api(search_schema: schemas.TopKSearchRequest):
    result = await crud.create_topk_search(search_schema)
    return result 

@router.post("/create_rl_search", response_model=schemas.SearchResponse)
async def create_rl_search_api(search_schema: schemas.RLSearchRequest):
    result = await crud.create_rl_search(search_schema)
    return result 

@router.get("/get/{search_id}", response_model=schemas.SearchResponse)
async def get_api(search_id: str, include_request: bool=True):
    item = await crud.get_search(search_id, include_request)
    return item 

@router.delete("/delete/{search_id}")
async def delete_api(search_id: str):
    item = await crud.delete_search(search_id)
    return item 

@router.get("/scroll", response_model=list[schemas.SearchResponse])
async def scroll_api(skip: int=0, limit: int=100, include_request: bool=True):
    items = await crud.scroll_search(skip, limit, include_request)
    return items 

@router.get("/get_results/{search_id}")
async def get_api(search_id: str, skip: int=0, limit: int=10):
    item = await crud.get_results(search_id, skip, limit)
    return item 

@router.get("/get_batch_log/{search_id}")
async def get_api(search_id: str, skip: int=0, limit: int=1):
    item = await crud.get_batch_log(search_id, skip, limit)
    return item 



