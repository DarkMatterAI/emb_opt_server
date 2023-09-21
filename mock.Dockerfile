FROM python:3.9-slim

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./mock /code/mock

CMD uvicorn mock.main:app --host $MOCK_HOST --port $MOCK_PORT --workers $MOCK_WORKERS --timeout-keep-alive $MOCK_TIMEOUT
