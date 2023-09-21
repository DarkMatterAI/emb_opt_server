import os
import time

from celery import Celery


broker = os.environ.get("CELERY_BROKER_URL", None)
backend = os.environ.get("CELERY_RESULT_BACKEND", None)
task_routes = {".create_search" : {'queue' : 'search_queue'}}

celery = Celery(__name__, backend=backend, broker=broker, task_routes=task_routes)


@celery.task(name="create_search")
def create_search(task_type):
    time.sleep(int(task_type) * 10)
    return True

