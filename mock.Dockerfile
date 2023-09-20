FROM python:3.9-slim

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./mock /code/mock

ENV MOCK_PORT=7888
ENV MOCK_HOST=0.0.0.0
ENV MOCK_WORKERS=1
ENV MOCK_TIMEOUT=120

CMD uvicorn mock.main:app --host $MOCK_HOST --port $MOCK_PORT --workers $MOCK_WORKERS --timeout-keep-alive $MOCK_TIMEOUT
