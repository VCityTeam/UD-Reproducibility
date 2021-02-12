FROM python:3.8

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY python-setup.py ./
COPY data-import ./



CMD ["/usr/bin/python3","/python_setup/setup.py","--bimServerConfig","/python_setup/bimServerConfig.yml","--ifc","/python_setup/carl.ifc","--projectName","carl","--ifcExtension","ifc4"]

