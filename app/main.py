from fastapi import FastAPI, responses
from .config import CONFIG

app = FastAPI(default_response_class=responses.ORJSONResponse)

@app.get("/")
def read_root():
    return {"Hello": "World"}