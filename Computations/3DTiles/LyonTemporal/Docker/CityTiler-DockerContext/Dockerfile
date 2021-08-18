# References
# - on chosing your Python base container
#   https://pythonspeed.com/articles/base-image-python-docker-images/
#   https://stackoverflow.com/questions/52740556/python-3-7-docker-images

FROM python:3.7-buster

RUN set -ex \
    && git clone https://github.com/VCityTeam/py3dtilers.git \
    && mv py3dtilers/ py3dtilers.git \
    && cd py3dtilers.git \
    && git checkout CityTiler_with_LodTree \
    && apt-get update \
    && apt-get install -y liblas-c3 libopenblas-base \
    && apt-get install -y libpq-dev \ 
    && pip install -e . \
    && pip install pyyaml \
    && python setup.py install

# Optionnal testing
#RUN set -ex \
#    && pip install pytest pytest-benchmark \
#    && pytest

WORKDIR py3dtilers.git/

# Copy the configuration files that are encountered the context
COPY ./CityTilerDBConfig*.yml py3dtilers/CityTiler/
COPY ./entrypoint.py ./

ENTRYPOINT ["python3", "./entrypoint.py"] 
