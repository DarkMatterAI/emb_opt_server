import numpy as np
import string
import requests 

from emb_opt.data_source import NumpyDataPlugin
from emb_opt.schemas import Query, Item, ScoreResponse, FilterResponse

from .create_endpoints import create_endpoints, MAIN_URL


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

def filter_plugin(inputs: list[Item]) -> list[FilterResponse]:
    return [FilterResponse(valid=i.data['rand']<0.9, data={'rand':i.data['rand']}) for i in inputs]

def filter_plugin_response(item_requests):
    items = [Item.from_minimal(**i.model_dump()) for i in item_requests]
    res = filter_plugin(items)
    return res 

def score_embeddings(embeddings: np.ndarray, sigma: float=5.) -> np.ndarray:
    target_point = np.ones(embeddings.shape[1])*.75
    
    distances = np.linalg.norm(embeddings - target_point, axis=1) / np.sqrt(embeddings.shape[1])
    
    scores = np.exp(-0.5 * (distances/sigma)**2)
        
    return scores

def score_plugin(inputs: list[Item]) -> list[ScoreResponse]:
    embeddings = np.array([i.embedding for i in inputs])
    scores = score_embeddings(embeddings)    
    results = [ScoreResponse(valid=True, score=i, data=None) for i in scores]
    return results

def score_plugin_response(item_requests):
    items = [Item.from_minimal(**i.model_dump()) for i in item_requests]
    res = score_plugin(items)
    return res 


def test_invoke():
    output = {'data_source':False, 'filter':False, 'score':False}
    endpoint_id_dict = create_endpoints()

    data_input = [{'item':'blah', 'embedding':np.random.randn(64).tolist(), 'data':{}}]

    data_result = requests.post(f"{MAIN_URL}/invoke/{endpoint_id_dict['data_source']}",
                            json=data_input).json()
    
    output['data_source'] = True

    filter_input = data_result[0]['query_results']

    filter_result = requests.post(f"{MAIN_URL}/invoke/{endpoint_id_dict['filter']}",
                            json=filter_input).json()

    output['filter'] = True

    score_input = [filter_input[i] for i in range(len(filter_input)) if filter_result[i]['valid']]

    score_result = requests.post(f"{MAIN_URL}/invoke/{endpoint_id_dict['score']}",
                            json=score_input).json()

    output['score'] = True

    return output
