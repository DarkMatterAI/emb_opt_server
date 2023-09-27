from fastapi.testclient import TestClient
import os 
import pytest
import copy
from app.tests.utils import *

def test_read_main(client: TestClient):
    response = client.get("/")
    assert response.status_code == 200


# crud helpers

def _create_endpoint_helper(endpoint_data, client):
    response = client.post("/create_endpoint", json=endpoint_data)
    assert response.status_code == 200
    response_dict = response.json()
    endpoint_id = response_dict['_id']
    for key in endpoint_data.keys():
        assert endpoint_data[key] == response_dict[key]
    return endpoint_id 

def _get_endpoint_helper(endpoint_id, client):
    response = client.get(f'/get/{endpoint_id}')
    assert response.status_code == 200
    response_dict = response.json()
    return response_dict 

def _update_endpoint_helper(endpoint_id, endpoint_data, client):
    response = client.post(f"/update/{endpoint_id}", json=endpoint_data)
    assert response.status_code == 200
    response_dict = response.json()
    for key in endpoint_data.keys():
        assert endpoint_data[key] == response_dict[key]

def _delete_endpoint_helper(endpoint_id, client):
    response = client.delete(f'/delete/{endpoint_id}')
    assert response.status_code == 200

def test_crud_functions(client: TestClient):
    
    # create
    endpoint_id = _create_endpoint_helper(test_create_endpoint, client)

    # read
    response_dict = _get_endpoint_helper(endpoint_id, client)
    for key in test_create_endpoint.keys():
        assert response_dict[key] == test_create_endpoint[key]

    # update
    _update_endpoint_helper(endpoint_id, test_update_endpoint, client)

    # delete
    _delete_endpoint_helper(endpoint_id, client)

def _invalid_create_helper(create_data, client):
    response = client.post("/create_endpoint", json=create_data)
    assert response.status_code != 200

def test_create_invalid_concurrency(client: TestClient):
    _invalid_create_helper(test_invalid_concurrency, client)

def test_create_invalid_batch_size(client: TestClient):
    _invalid_create_helper(test_invalid_batch_size, client)

def test_create_invalid_url(client: TestClient):
    _invalid_create_helper(test_invalid_url, client)

def test_create_invalid_required_fields(client: TestClient):
    _invalid_create_helper(test_invalid_required_fields, client)

def test_create_invalid_endpoint_type(client: TestClient):
    _invalid_create_helper(test_invalid_type, client)

