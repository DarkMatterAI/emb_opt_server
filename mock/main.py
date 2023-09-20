from typing import Annotated, List
from fastapi import FastAPI, responses, Body
import requests 

from . import plugins, schemas 

app = FastAPI(default_response_class=responses.ORJSONResponse)

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/ping_main")
def ping_main():
    return requests.get(f'{plugins.MAIN_URL}/').json()

@app.post("/data_source", response_model=List[schemas.DataSourceResponse])
def mock_data_source(inputs: List[schemas.QueryRequest]):
    return plugins.data_plugin_response(inputs)

@app.post("/filter", response_model=List[schemas.FilterResponse])
def mock_filter(inputs: List[schemas.ItemRequest]):
    return plugins.filter_plugin_response(inputs)

@app.post("/score", response_model=List[schemas.ScoreResponse])
def mock_score(inputs: List[schemas.ItemRequest]):
    return plugins.score_plugin_response(inputs)

