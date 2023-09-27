from fastapi.testclient import TestClient
import os 
import pytest
import copy
import requests 
import time 

from mock.tests.utils import *

def test_read_main(client: TestClient):
    response = client.get("/")
    assert response.status_code == 200

def test_ping_server(client: TestClient):
    response = requests.get(f'{MAIN_URL}/')
    assert response.status_code == 200

def test_invoke_data_source(client: TestClient):
    data_input = [{'item':'blah', 'embedding':INITIAL_EMBEDDING, 'data':{}}]
    response = requests.post(f"{MAIN_URL}/invoke/{ENDPOINT_DICT['data_source']}",
                            json=data_input)
    assert response.status_code == 200

def test_invoke_filter(client: TestClient):
    data_input = [{'item':'blah', 'embedding':INITIAL_EMBEDDING, 'data':{}}]
    data_result = requests.post(f"{MAIN_URL}/invoke/{ENDPOINT_DICT['data_source']}",
                            json=data_input).json()

    filter_input = data_result[0]['query_results']
    response = requests.post(f"{MAIN_URL}/invoke/{ENDPOINT_DICT['filter']}",
                            json=filter_input)

    assert response.status_code == 200

def test_invoke_score(client: TestClient):
    data_input = [{'item':'blah', 'embedding':INITIAL_EMBEDDING, 'data':{}}]
    data_result = requests.post(f"{MAIN_URL}/invoke/{ENDPOINT_DICT['data_source']}",
                            json=data_input).json()

    score_input = data_result[0]['query_results']
    response = requests.post(f"{MAIN_URL}/invoke/{ENDPOINT_DICT['score']}",
                            json=score_input)

    assert response.status_code == 200

def _create_search_helper(create_search_data, search_endpoint):
    response = requests.post(f"{MAIN_URL}/search/{search_endpoint}", json=create_search_data)
    assert response.status_code == 200
    search_data = response.json()
    search_id = search_data["_id"]
    return search_id 

def _await_search_helper(search_id):
    for i in range(20):
        response = requests.get(f"{MAIN_URL}/search/get/{search_id}", params={'include_request':False})
        assert response.status_code == 200
        response_data = response.json()
        search_status = response_data['search_data']['status']

        if search_status == 'finished':
            return True 
        else:
            time.sleep(1.0)

    raise Exception('search failed to complete')

def _get_search_resuts_helper(search_id, skip, limit):
    response = requests.get(f"{MAIN_URL}/search/get_results/{search_id}", params={'skip':skip, 'limit':limit})
    assert response.status_code == 200
    response_data = response.json()
    assert len(response_data)>0

def _get_search_batch_log_helper(search_id, skip, limit):
    response = requests.get(f"{MAIN_URL}/search/get_batch_log/{search_id}", params={'skip':skip, 'limit':limit})
    assert response.status_code == 200
    response_data = response.json()
    assert len(response_data)>0

def _delete_search_helper(search_id):
    response = requests.delete(f"{MAIN_URL}/search/delete/{search_id}")
    assert response.status_code == 200

def _search_test_helper(create_search_data, search_endpoint):
    search_id = _create_search_helper(create_search_data, search_endpoint)
    _await_search_helper(search_id)
    _get_search_resuts_helper(search_id, 0, 1)
    _get_search_batch_log_helper(search_id, 0, 1)
    _delete_search_helper(search_id)
    
# def test_topk_search_basic_continuous(client: TestClient):
#     _search_test_helper(topk_search_basic_continuous, 'create_topk_search')

# def test_topk_search_basic_discrete(client: TestClient):
#     _search_test_helper(topk_search_basic_discrete, 'create_topk_search')

# def test_topk_search_discrete_prune_mean(client: TestClient):
#     _search_test_helper(topk_search_discrete_prune_mean, 'create_topk_search')

# def test_topk_search_discrete_prune_max(client: TestClient):
#     _search_test_helper(topk_search_discrete_prune_max, 'create_topk_search')

# def test_topk_search_grad_query(client: TestClient):
#     _search_test_helper(topk_search_grad_query, 'create_topk_search')

# def test_topk_search_grad_query_dp(client: TestClient):
#     _search_test_helper(topk_search_grad_query_dp, 'create_topk_search')

# def test_topk_search_grad_query_norm(client: TestClient):
#     _search_test_helper(topk_search_grad_query_norm, 'create_topk_search')

# def test_rl_search_basic(client: TestClient):
#     _search_test_helper(rl_search_basic, 'create_rl_search')

# def test_rl_search_prune(client: TestClient):
#     _search_test_helper(rl_search_prune, 'create_rl_search')

# def test_rl_search_dp(client: TestClient):
#     _search_test_helper(rl_search_dp, 'create_rl_search')

# def test_rl_search_norm(client: TestClient):
#     _search_test_helper(rl_search_norm, 'create_rl_search')


def _invalid_search_helper(create_search_data, search_endpoint):
    response = requests.post(f"{MAIN_URL}/search/{search_endpoint}", json=create_search_data)
    assert response.status_code != 200

def test_invalid_data_source(client: TestClient):
    _invalid_search_helper(invalid_data_source, 'create_topk_search')

def test_invalid_filter(client: TestClient):
    _invalid_search_helper(invalid_filter, 'create_topk_search')

def test_invalid_score(client: TestClient):
    _invalid_search_helper(invalid_score, 'create_topk_search')

def test_invalid_update_k(client: TestClient):
    _invalid_search_helper(invalid_update_k, 'create_topk_search')

def test_invalid_update_type(client: TestClient):
    _invalid_search_helper(invalid_update_type, 'create_topk_search')

def test_invalid_prune_k(client: TestClient):
    _invalid_search_helper(invalid_prune_k, 'create_topk_search')

def test_invalid_prune_agg(client: TestClient):
    _invalid_search_helper(invalid_prune_agg, 'create_topk_search')

def test_invalid_prune_group(client: TestClient):
    _invalid_search_helper(invalid_prune_group, 'create_topk_search')


