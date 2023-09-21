import numpy as np
import string
import requests 
from typing import List 

from emb_opt.data_source import NumpyDataPlugin
from emb_opt.schemas import Query, Item, ScoreResponse, FilterResponse


MAIN_URL = "http://emb_opt_server:7861"

data_create = {
  "name": "mock_data_source",
  "endpoint_data": {
    "url": "http://mock_server:7888/data_source",
    "concurrency": 1,
    "batch_size": 10
  },
  "request_data": {
    "item": False,
    "embedding": True 
  }
}

filter_create = {
  "name": "mock_filter",
  "endpoint_data": {
    "url": "http://mock_server:7888/filter",
    "concurrency": 1,
    "batch_size": 10
  },
  "request_data": {
    "item": True,
    "embedding": True,
    "data": True
  }
}

score_create = {
  "name": "mock_score",
  "endpoint_data": {
    "url": "http://mock_server:7888/score",
    "concurrency": 1,
    "batch_size": 10
  },
  "request_data": {
    "item": True,
    "embedding": True,
    "data": False
  }
}

def setup_endpoints():
    r1 = requests.post(f'{MAIN_URL}/data_source/create', json=data_create)
    r2 = requests.post(f'{MAIN_URL}/filter/create', json=filter_create)
    r3 = requests.post(f'{MAIN_URL}/score/create', json=score_create)

    return r1.json()['_id'], r2.json()['_id'], r3.json()['_id']

def get_data_plugin():
    n_vectors = 1000
    size = 64

    np.random.seed(42)
    vectors = np.random.randn(n_vectors, size)

    vector_data = [{
                    'index' : i,
                    'item' : ''.join(np.random.choice([i for i in string.ascii_lowercase], size=10).tolist()),
                    'rand' : np.random.rand(),
                } for i in range(n_vectors)]

    data_plugin = NumpyDataPlugin(10, vectors, vector_data, 'index', 'item')
    return data_plugin 

DATA_PLUGIN = get_data_plugin()

def data_plugin_response(query_requests):
    queries = [Query.from_minimal(**i.model_dump()) for i in query_requests]
    res = DATA_PLUGIN(queries)
    return res 

def score_embeddings(embeddings: np.ndarray, sigma: float=5.) -> np.ndarray:
    target_point = np.ones(embeddings.shape[1])*.75
    
    distances = np.linalg.norm(embeddings - target_point, axis=1) / np.sqrt(embeddings.shape[1])
    
    scores = np.exp(-0.5 * (distances/sigma)**2)
        
    return scores

def score_plugin(inputs: List[Item]) -> List[ScoreResponse]:
    embeddings = np.array([i.embedding for i in inputs])
    scores = score_embeddings(embeddings)    
    results = [ScoreResponse(valid=True, score=i, data=None) for i in scores]
    return results

def score_plugin_response(item_requests):
    items = [Item.from_minimal(**i.model_dump()) for i in item_requests]
    res = score_plugin(items)
    return res 

def filter_plugin(inputs: List[Item]) -> List[FilterResponse]:
    return [FilterResponse(valid=i.data['rand']<0.9, data={'rand':i.data['rand']}) for i in inputs]

def filter_plugin_response(item_requests):
    items = [Item.from_minimal(**i.model_dump()) for i in item_requests]
    res = filter_plugin(items)
    return res 