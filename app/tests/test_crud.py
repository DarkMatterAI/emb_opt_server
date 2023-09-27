from fastapi.testclient import TestClient
import os 
import pytest
import copy

def test_read_main(client: TestClient):
    response = client.get("/")
    assert response.status_code == 200
