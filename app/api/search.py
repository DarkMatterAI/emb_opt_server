from fastapi import APIRouter, responses
from .. import crud 
from ..schemas import schemas_search 

router = APIRouter(default_response_class=responses.ORJSONResponse)

@router.post("/create_topk_search")
async def create_topk_search_api(search_schema: schemas_search.TopKSearchRequest):
    result = await crud.create_topk_search(search_schema)
    return result 

@router.post("/create_rl_search")
async def create_rl_search_api(search_schema: schemas_search.RLSearchRequest):
    result = await crud.create_rl_search(search_schema)
    return result 

