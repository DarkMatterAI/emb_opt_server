#!/bin/sh

if [ "$CONTAINER_ROLE" = "server" ]; then
    uvicorn app.main:app --host $EMB_OPT_HOST --port $EMB_OPT_PORT --workers $EMB_OPT_WORKERS --timeout-keep-alive $EMB_OPT_TIMEOUT
elif [ "$CONTAINER_ROLE" = "worker" ]; then
    celery -A app.worker.celery_worker.celery worker --loglevel=info --concurrency $CELERY_WORKER_CONCURRENCY -n search_worker@%h -Q search_queue
else
    echo "Unknown CONTAINER_ROLE: $CONTAINER_ROLE"
    exit 1
fi