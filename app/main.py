from fastapi import FastAPI, responses
from .database import init_mongodb

from . import api 

app = FastAPI(default_response_class=responses.ORJSONResponse)

app.include_router(api.data_source.router, prefix='/data_source', tags=["data_source"])
app.include_router(api.filter.router, prefix='/filter', tags=["filter"])
app.include_router(api.score.router, prefix='/score', tags=["score"])

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.on_event("startup")
async def init_db():
    await init_mongodb()
