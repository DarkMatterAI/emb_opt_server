from fastapi import FastAPI, responses
from .database import init_mongodb
from . import schemas, crud, api

app = FastAPI(default_response_class=responses.ORJSONResponse)

app.include_router(api.crud_api.router, tags=["endpoint"])
app.include_router(api.search_api.router, prefix='/search', tags=["search"])

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.on_event("startup")
async def init_db():
    await init_mongodb()
