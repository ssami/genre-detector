#
FROM python:3.9

#
WORKDIR /code

#
COPY requirements.txt /code/requirements.txt

#
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app
COPY ./app/lib /code/app/lib
COPY genre_class_1590302222.bin /code/app/model.bin

#
CMD ["uvicorn", "app.infer:app", "--host", "0.0.0.0", "--port", "80"]
