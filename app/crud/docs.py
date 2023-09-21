DATA_SOURCE_DOCS = '''
A data source runs an embedding query and returns a set of query results

creation schema: 

```
creation_schema = {
                    "endpoint_data": {
                        "name": "string",
                        "url": "https://example.com/",
                        "concurrency": 1,
                        "batch_size": 1
                    },
                    "required_fields": {
                        "item": true,
                        "embedding": true,
                        "data": true
                    },
                    "endpoint_type": "data_source"
                    }
```

When invoked, the `url` will be called with `concurrent` concurrent requests with 
`batch_size` items per request. Creation schema requires `concurrent>0, batch_size>0`.

Requests send data with the following schema:

```
request_schema = [
                    {
                    "item" : Optional[str],
                    "embedding" : Optional[list[float]],
                    "data" : Optional[dict]
                    }
                ]
```

The request fields `item`, `embedding` and `data` will be `None` if the 
corresponding field in the creation schema is set to `False`

The endpoint is expected to return the following response format:

```
item_response_schema = {
    "id" : Optional[Union[str, int]]
    "item" : Optional[str],
    "embedding" : list[float],
    "data" : Optional[dict]
}

data_source_response_schema = {
    "valid" : bool,
    "data" : dict,
    "query_results" : list[item_response_schema]
}

function_schema = Callable[query_request_schema, List[data_response_schema]]
```
'''

FILTER_DOCS = '''
A filter evaluates an item based on some true/false criteria

creation schema: 

```
creation_schema = {
                    "endpoint_data": {
                        "name": "string",
                        "url": "https://example.com/",
                        "concurrency": 1,
                        "batch_size": 1
                    },
                    "required_fields": {
                        "item": true,
                        "embedding": true,
                        "data": true
                    },
                    "endpoint_type": "data_source"
                    }
```

When invoked, the `url` will be called with `concurrent` concurrent requests with 
`batch_size` items per request. Creation schema requires `concurrent>0, batch_size>0`.

Requests send data with the following schema:

```
request_schema = [
                    {
                    "item" : Optional[str],
                    "embedding" : Optional[list[float]],
                    "data" : Optional[dict]
                    }
                ]
```

The request fields `item`, `embedding` and `data` will be `None` if the 
corresponding field in the creation schema is set to `False`

The endpoint is expected to return the following response format:

```
filter_response_schema = {
    "valid" : bool,
    "data" : dict
}

function_schema = Callable[request_schema, List[filter_response_schema]]
```
'''


SCORE_DOCS = '''
A score assigns a numerical score to an item

creation schema: 

```
creation_schema = {
                    "endpoint_data": {
                        "name": "string",
                        "url": "https://example.com/",
                        "concurrency": 1,
                        "batch_size": 1
                    },
                    "required_fields": {
                        "item": true,
                        "embedding": true,
                        "data": true
                    },
                    "endpoint_type": "data_source"
                    }
```

When invoked, the `url` will be called with `concurrent` concurrent requests with 
`batch_size` items per request. Creation schema requires `concurrent>0, batch_size>0`.

Requests send data with the following schema:

```
request_schema = [
                    {
                    "item" : Optional[str],
                    "embedding" : Optional[list[float]],
                    "data" : Optional[dict]
                    }
                ]
```

The request fields `item`, `embedding` and `data` will be `None` if the 
corresponding field in the creation schema is set to `False`

The endpoint is expected to return the following response format:

```
score_response_schema = {
    "valid" : bool,
    "score" : float,
    "data" : dict
}

function_schema = Callable[request_schema, List[score_response_schema]]
```
'''

DOCS_MAPPING = {
    'data_source' : DATA_SOURCE_DOCS,
    'filter' : FILTER_DOCS,
    'score' : SCORE_DOCS
}


