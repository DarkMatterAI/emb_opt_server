from fastapi import APIRouter, responses
from .. import schemas, crud 

router = APIRouter(default_response_class=responses.ORJSONResponse)

@router.post("/invoke/{endpoint_id}")
async def invoke_api(endpoint_id: str, invoke_data: list[schemas.InvokeItem]):
    results = await crud.invoke_endpoint(endpoint_id, invoke_data)
    return results   

@router.post("/create_topk_search")
async def create_topk_search_api(search_schema: schemas.TopKSearchRequest):
    result = await crud.create_topk_search(search_schema)
    return result 

@router.post("/create_rl_search")
async def create_rl_search_api(search_schema: schemas.RLSearchRequest):
    result = await crud.create_rl_search(search_schema)
    return result 



# topk search
# rl search
