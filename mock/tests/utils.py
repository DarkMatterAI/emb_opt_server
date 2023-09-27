import os 
import copy
import numpy as np 
from mock.create_endpoints import create_endpoints

MAIN_URL = f"http://emb_opt_server:{os.environ.get('EMB_OPT_PORT')}"
ENDPOINT_DICT = create_endpoints()
EMBEDDING_SIZE = 64
np.random.seed(42)
INITIAL_EMBEDDING = np.random.randn(EMBEDDING_SIZE).tolist()

topk_base = {
  "data_source_id": ENDPOINT_DICT['data_source'],
  "filter_id": ENDPOINT_DICT['filter'],
  "score_id": ENDPOINT_DICT['score'],
  "prune_schema": None,
  "update_schema": None,
  "iterations": 2,
  "initial_embeddings": [INITIAL_EMBEDDING],
  "grad_query": None
}

topk_update_continuous = {"update_k": 3, "update_type": "continuous"}
topk_update_discrete = {"update_k": 3, "update_type": "discrete"}

prune_mean = {"k": 1, "score_agg": "mean", "group_by": "collection_id"}
prune_max = {"k": 1, "score_agg": "max", "group_by": "collection_id"}

grad_basic = {"lrs": [0.1, 0.5, 1.0], "distance_penalty": None,
              "max_norm": None, "norm_type": None}

grad_single = {"lrs": [0.1], "distance_penalty": None,
              "max_norm": None, "norm_type": None}

grad_dp = {"lrs": [0.1, 0.5, 1.0], "distance_penalty": 0.1,
           "max_norm": None, "norm_type": None}

grad_norm = {"lrs": [0.1, 0.5, 1.0], "distance_penalty": None,
             "max_norm": 1.0, "norm_type": 2}

def build_search_test_schema(base, kwargs):
    schema = copy.deepcopy(base)
    for k,v in kwargs.items():
        schema[k] = copy.deepcopy(v)
    return schema 

topk_search_basic_continuous = build_search_test_schema(topk_base, 
                                    {'update_schema' : topk_update_continuous})

topk_search_basic_discrete = build_search_test_schema(topk_base, 
                                    {'update_schema' : topk_update_discrete})

topk_search_discrete_prune_mean = build_search_test_schema(topk_base, 
                                    {'update_schema' : topk_update_discrete,
                                     'prune_schema' : prune_mean})

topk_search_discrete_prune_max = build_search_test_schema(topk_base, 
                                    {'update_schema' : topk_update_discrete,
                                     'prune_schema' : prune_max})

topk_search_grad_query = build_search_test_schema(topk_base, 
                                    {'update_schema' : topk_update_continuous,
                                     'prune_schema' : prune_mean,
                                     'grad_query' : grad_basic})

topk_search_grad_query_dp = build_search_test_schema(topk_base, 
                                    {'update_schema' : topk_update_continuous,
                                     'prune_schema' : prune_mean,
                                     'grad_query' : grad_dp})

topk_search_grad_query_norm = build_search_test_schema(topk_base, 
                                    {'update_schema' : topk_update_continuous,
                                     'prune_schema' : prune_mean,
                                     'grad_query' : grad_norm})


rl_base = {
  "data_source_id": ENDPOINT_DICT['data_source'],
  "filter_id": ENDPOINT_DICT['filter'],
  "score_id": ENDPOINT_DICT['score'],
  "prune_schema": None,
  "update_schema": None,
  "iterations": 2,
  "initial_embeddings": [INITIAL_EMBEDDING],
}

rl_search_basic = build_search_test_schema(rl_base, {'update_schema' : grad_single})

rl_search_prune = build_search_test_schema(rl_base, 
                                    {'prune_schema' : prune_mean,
                                     'update_schema' : grad_basic})

rl_search_dp = build_search_test_schema(rl_base, 
                                    {'prune_schema' : prune_mean,
                                     'update_schema' : grad_dp})

rl_search_norm = build_search_test_schema(rl_base, 
                                    {'prune_schema' : prune_mean,
                                     'update_schema' : grad_norm})


topk_invalid_base = {
  "data_source_id": ENDPOINT_DICT['data_source'],
  "filter_id": ENDPOINT_DICT['filter'],
  "score_id": ENDPOINT_DICT['score'],
  "prune_schema": None,
  "update_schema": {"update_k": 3, "update_type": "continuous"},
  "iterations": 2,
  "initial_embeddings": [INITIAL_EMBEDDING],
  "grad_query": None
}

topk_update_invalid_k = {"update_k": 0, "update_type": "continuous"}
topk_update_invalid_type = {"update_k": 1, "update_type": "werg"}

prune_invalid_k = {"k": 0, "score_agg": "mean", "group_by": "collection_id"}
prune_invalid_agg = {"k": 1, "score_agg": "dgrsbfvd", "group_by": "collection_id"}
prune_invalid_group = {"k": 1, "score_agg": "mean", "group_by": "sfg d"}


invalid_data_source = build_search_test_schema(topk_invalid_base, 
                                    {'data_source_id' : '651461f90ac21cf3e937e9f7'})

invalid_filter= build_search_test_schema(topk_invalid_base, 
                                    {'filter_id' : '651461f90ac21cf3e937e9f7'})

invalid_score = build_search_test_schema(topk_invalid_base, 
                                    {'score_id' : '651461f90ac21cf3e937e9f7'})

invalid_update_k = build_search_test_schema(topk_invalid_base, 
                                    {'update_schema' : topk_update_invalid_k})

invalid_update_type = build_search_test_schema(topk_invalid_base, 
                                    {'update_schema' : topk_update_invalid_type})

invalid_prune_k = build_search_test_schema(topk_invalid_base, 
                                    {'prune_schema' : prune_invalid_k})

invalid_prune_agg = build_search_test_schema(topk_invalid_base, 
                                    {'prune_schema' : prune_invalid_agg})

invalid_prune_group = build_search_test_schema(topk_invalid_base, 
                                    {'prune_schema' : prune_invalid_group})
