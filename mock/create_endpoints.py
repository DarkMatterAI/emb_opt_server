import os 
import requests 
import time 

MAIN_URL = f"http://emb_opt_server:{os.environ.get('EMB_OPT_PORT')}"
SELF_URL = f"http://mock_server:{os.environ.get('MOCK_PORT')}"


data_create_schema = {
  "endpoint_data": {
    "name": "mock_data_source",
    "url": f"{SELF_URL}/data_source",
    "concurrency": 1,
    "batch_size": 10
  },
  "required_fields": {
    "item": False,
    "embedding": True,
    "data": False
  },
  "endpoint_type": "data_source"
}

filter_create_schema = {
  "endpoint_data": {
    "name": "mock_filter",
    "url": f"{SELF_URL}/filter",
    "concurrency": 1,
    "batch_size": 10
  },
  "required_fields": {
    "item": True,
    "embedding": True,
    "data": True
  },
  "endpoint_type": "filter"
}

score_create_schema = {
  "endpoint_data": {
    "name": "mock_score",
    "url": f"{SELF_URL}/score",
    "concurrency": 1,
    "batch_size": 10
  },
  "required_fields": {
    "item": True,
    "embedding": True,
    "data": False
  },
  "endpoint_type": "score"
}


all_create_schemas = [
    data_create_schema,
    filter_create_schema,
    score_create_schema
]

def create_endpoints():
    time.sleep(3)
    outputs = {}
    for create_schema in all_create_schemas:
        name = create_schema['endpoint_data']['name']
        current_endpoints = requests.get(f'{MAIN_URL}/scroll_by_name', 
             params={'skip':0,'limit':100, 'endpoint_name':name}
            ).json()
        
        if len(current_endpoints)==0:
            create_result = requests.post(f'{MAIN_URL}/create_endpoint', json=create_schema)
            endpoint_id = create_result.json()['_id']
        else:
            endpoint_id = current_endpoints[0]['_id']

        print(create_schema['endpoint_type'], endpoint_id)

        outputs[create_schema['endpoint_type']] = endpoint_id

    return outputs



