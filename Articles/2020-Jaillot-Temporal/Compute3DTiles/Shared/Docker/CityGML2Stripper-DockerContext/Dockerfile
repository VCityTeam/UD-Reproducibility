# References
# - on chosing your Python base container
#   https://pythonspeed.com/articles/base-image-python-docker-images/
#   https://stackoverflow.com/questions/52740556/python-3-7-docker-images

FROM python:3.7-buster

RUN  set -ex \
     && git clone https://github.com/VCityTeam/UD-Serv.git \
     && cd UD-Serv/Utils/CityGML2Stripper \
     && pip install -r requirements.txt \
     && mkdir /src \
     && cp CityGML2Stripper.py /src

ENTRYPOINT ["python", "/src/CityGML2Stripper.py"] 
