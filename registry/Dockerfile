FROM python:3.9


COPY setup.sh ./setup.sh

RUN chmod +x ./setup.sh

RUN ./setup.sh

CMD mlflow server
