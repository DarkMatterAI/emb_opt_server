from fastapi import FastAPI, responses
from .create_endpoints import create_endpoints
from . import plugins, schemas

app = FastAPI(default_response_class=responses.ORJSONResponse)

@app.on_event("startup")
def create_endpoints_api():
    create_endpoints()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/data_source", response_model=list[schemas.DataSourceResponse])
def mock_data_source(inputs: list[schemas.InvokeItem]):
    return plugins.data_plugin_response(inputs)

@app.post("/filter", response_model=list[schemas.FilterResponse])
def mock_filter(inputs: list[schemas.InvokeItem]):
    return plugins.filter_plugin_response(inputs)

@app.post("/score", response_model=list[schemas.ScoreResponse])
def mock_score(inputs: list[schemas.InvokeItem]):
    return plugins.score_plugin_response(inputs)

@app.get("/test_invoke")
def test_invoke_api():
    return plugins.test_invoke()