FROM python:3.8

WORKDIR /usr/src/app

COPY requirements.txt ./
COPY python-setup.py ./
COPY data_import ./data_import

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python","-u","python-setup.py"]