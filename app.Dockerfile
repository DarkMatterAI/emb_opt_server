FROM python:3.9-slim

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app

ENV EMB_OPT_PORT=7860
ENV EMB_OPT_HOST=0.0.0.0
ENV EMB_OPT_WORKERS=1
ENV EMB_OPT_TIMEOUT=120
ENV MONGO_URI=
ENV MONGO_DB_NAME=emb_opt_db
ENV CELERY_BROKER_URL=
ENV CELERY_RESULT_BACKEND=

CMD uvicorn app.main:app --host $EMB_OPT_HOST --port $EMB_OPT_PORT --workers $EMB_OPT_WORKERS --timeout-keep-alive $EMB_OPT_TIMEOUT
