
test_create_endpoint = {
  "endpoint_data": {
    "name": "string",
    "url": "https://example.com/",
    "concurrency": 1,
    "batch_size": 1
  },
  "required_fields": {
    "item": True,
    "embedding": True,
    "data": True
  },
  "endpoint_type": "data_source"
}

test_update_endpoint = {
  "endpoint_data": {
    "name": "string",
    "url": "https://example2.com/",
    "concurrency": 5,
    "batch_size": 10
  },
  "required_fields": {
    "item": True,
    "embedding": True,
    "data": False
  },
  "endpoint_type": "data_source"
}

test_invalid_concurrency = {
  "endpoint_data": {
    "name": "string",
    "url": "https://example.com/",
    "concurrency": 0,
    "batch_size": 1
  },
  "required_fields": {
    "item": True,
    "embedding": True,
    "data": True
  },
  "endpoint_type": "data_source"
}

test_invalid_batch_size = {
  "endpoint_data": {
    "name": "string",
    "url": "https://example.com/",
    "concurrency": 1,
    "batch_size": 0
  },
  "required_fields": {
    "item": True,
    "embedding": True,
    "data": True
  },
  "endpoint_type": "data_source"
}

test_invalid_url = {
  "endpoint_data": {
    "name": "string",
    "url": "acvsdfbgh",
    "concurrency": 1,
    "batch_size": 1
  },
  "required_fields": {
    "item": True,
    "embedding": True,
    "data": True
  },
  "endpoint_type": "data_source"
}

test_invalid_required_fields = {
  "endpoint_data": {
    "name": "string",
    "url": "https://example.com/",
    "concurrency": 1,
    "batch_size": 1
  },
  "required_fields": {
    "item": False,
    "embedding": False,
    "data": False
  },
  "endpoint_type": "data_source"
}

test_invalid_type = {
  "endpoint_data": {
    "name": "string",
    "url": "https://example.com/",
    "concurrency": 1,
    "batch_size": 1
  },
  "required_fields": {
    "item": True,
    "embedding": True,
    "data": True
  },
  "endpoint_type": "svdbgfch"
}
