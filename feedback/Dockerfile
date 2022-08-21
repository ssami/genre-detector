FROM python:3.9

WORKDIR /code

COPY requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app

# build time args that are converted into env variables
# ARG values are defaults that can be overridden
ARG MONGO_HOST=127.0.0.1
ENV MONGO_HOST=$MONGO_HOST

ARG MONGO_PORT=27017
ENV MONGO_PORT=$MONGO_PORT

CMD ["uvicorn", "app.feedback:app", "--host", "some-mongo", "--port", "8080"]

# To build:
# docker build -t feedback --build-arg MONGO_HOST=<host> --build-arg MONGO_PORT=<port> .
# Expects to connect to a Mongo instance or another Docker container running Mongo
# at the specified MONGO_HOST:MONGO_PORT
