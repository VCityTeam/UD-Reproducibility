FROM python:3.8

WORKDIR /usr/src/app

ARG GEOSERVER_DATA_IMPORT_DIR
ENV GEOSERVER_DATA_IMPORT_DIR=${GEOSERVER_DATA_IMPORT_DIR}

ENV DATA_IMPORT_DIR=./data_import

COPY requirements.txt ./
COPY python_setup.py ./
COPY $GEOSERVER_DATA_IMPORT_DIR $DATA_IMPORT_DIR

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python","-u","python_setup.py"]
