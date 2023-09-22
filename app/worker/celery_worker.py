import os
import time
import logging
import asyncio

from celery import Celery

from .. import schemas 
from .search import run_search


broker = os.environ.get("CELERY_BROKER_URL", None)
backend = os.environ.get("CELERY_RESULT_BACKEND", None)
task_routes = {".create_search" : {'queue' : 'search_queue'}}

celery = Celery(__name__, backend=backend, broker=broker, task_routes=task_routes)
logger = logging.getLogger(__name__)


@celery.task(name="create_search")
def create_search(search_request_id: str):
    logger.info(search_request_id)
    asyncio.run(run_search(search_request_id))
    time.sleep(5)
    logger.info('done')
    # 1/0
    return True

