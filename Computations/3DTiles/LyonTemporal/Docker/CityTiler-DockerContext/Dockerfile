# References
# - on chosing your Python base container
#   https://pythonspeed.com/articles/base-image-python-docker-images/
#   https://stackoverflow.com/questions/52740556/python-3-7-docker-images

FROM python:3.7-buster

RUN set -ex \
    && git clone https://github.com/VCityTeam/py3dtiles.git \
    && git reset --hard a5a134e5bfbf4bacdd45200b2069e4f2ac3a5fce \
    && mv py3dtiles/ py3dtiles.git \
    && cd py3dtiles.git \
    && git checkout Tiler \
    && pip install -e . \
    && pip install pyyaml \
    && python setup.py install

# Optionnal testing
#RUN set -ex \
#    && pip install pytest pytest-benchmark \
#    && pytest

WORKDIR py3dtiles.git/

# Copy the configuration files that are encountered the context
COPY ./CityTilerDBConfig*.yml Tilers/CityTiler/
COPY ./entrypoint.py ./

ENTRYPOINT ["./entrypoint.py"] 
