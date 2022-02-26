FROM python:3.9

COPY requirements.txt ./requirements.txt

# short term solution to copy data into training Docker image
COPY raw.csv ./raw.csv

COPY train.py ./train.py

# short term solution until Python wheel is built for dependencies
COPY ./lib/ ./lib

RUN pip install --no-cache-dir --upgrade -r ./requirements.txt

# cmd with default or short-term values
CMD ["python", "train.py", "--csv", "raw.csv", "--fburl", "http://0.0.0.0:80/feedback"]
