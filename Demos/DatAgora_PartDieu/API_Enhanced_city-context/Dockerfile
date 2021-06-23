FROM python:3.6

LABEL maintainer "VCityTeam"
LABEL source.repo "https://github.com/VCityTeam/UD-Serv.git"

RUN apt-get update

ARG APIENHANCED=/UD-Serv/API_Enhanced_City/

RUN apt-get install -y git

RUN git clone https://github.com/VCityTeam/UD-Serv.git

WORKDIR $APIENHANCED

#.env probably used elsewhere and needs to be copied for now
COPY .env .env

RUN pip install -r requirements.txt

ENV PYTHONPATH $APIENHANCED

CMD ["python", "api/web_api.py"]