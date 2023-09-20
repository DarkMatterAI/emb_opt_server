
DATA_SOURCE_DOCS = '''
A data source runs an embedding query and returns a set of query results

```
creation_schema = {
  "name": "string",
  "endpoint_data": {
    "url": "https://example.com/",
    "concurrency": 1,
    "batch_size": 1
  },
  "request_data": {
    "item": true,
    "embedding": true
  }
}
```

Fields in `creation_schema.request_data` are included in the request if True, 
omitted if False. One of `creation_schema.request_data.item`, 
`creation_schema.request_data.embedding` must be `True`.

If `request_data.item==True`, data source is incompatible with gradient queries

Function calls will be made as a `post` request to `creation_schema.endpoint_data.url` 
with `concurrency` concurrent queries and `batch_size` queries per call.

The function is expected to correspond to the following schema:

```
query_request_schema = {
    "item" : Optional[str],
    "embedding" : list[float]
}

item_response_schema = {
    "item" : Optional[str],
    "embedding" : list[float],
    "data" : dict
}

data_response_schema = {
    "valid" : bool,
    "data" : dict,
    "query_results" : list[item_response_schema]
}

function_schema = Callable[list[query_request_schema], List[data_response_schema]]
```
'''

FILTER_DOCS = '''
A filter evaluates an item based on some true/false criteria

```
creation_schema = {
  "name": "string",
  "endpoint_data": {
    "url": "https://example.com/",
    "concurrency": 1,
    "batch_size": 1
  },
  "request_data": {
    "item": true,
    "embedding": true,
    "data" true
  }
}
```

Fields in `creation_schema.request_data` are included in the request if True, 
omitted if False. One of `creation_schema.request_data.item`, 
`creation_schema.request_data.embedding` must be `True`.

Function calls will be made as a `post` request to `creation_schema.endpoint_data.url` 
with `concurrency` concurrent queries and `batch_size` queries per call.

The function is expected to correspond to the following schema:

```
item_request_schema = {
    "item" : Optional[str],
    "embedding" : Optional[list[float]],
    "data" : dict
}

data_response_schema = {
    "valid" : bool,
    "data" : dict
}

function_schema = Callable[list[item_request_schema], List[data_response_schema]]
```
'''

SCORE_DOCS = '''
A score assigns a numerical score to an item

```
creation_schema = {
  "name": "string",
  "endpoint_data": {
    "url": "https://example.com/",
    "concurrency": 1,
    "batch_size": 1
  },
  "request_data": {
    "item": true,
    "embedding": true,
    "data" true
  }
}
```

Fields in `creation_schema.request_data` are included in the request if True, 
omitted if False. One of `creation_schema.request_data.item`, 
`creation_schema.request_data.embedding` must be `True`.

Function calls will be made as a `post` request to `creation_schema.endpoint_data.url` 
with `concurrency` concurrent queries and `batch_size` queries per call.

The function is expected to correspond to the following schema:

```
item_request_schema = {
    "item" : Optional[str],
    "embedding" : Optional[list[float]],
    "data" : dict
}

data_response_schema = {
    "valid" : bool,
    "score" : float,
    "data" : dict
}

function_schema = Callable[list[item_request_schema], List[data_response_schema]]
```
'''

