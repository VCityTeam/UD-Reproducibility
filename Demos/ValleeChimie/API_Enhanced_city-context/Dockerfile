FROM python:3.6

LABEL maintainer "VCityTeam"
LABEL source.repo "https://github.com/VCityTeam/UD-Viz-docker/"

RUN apt-get update

ARG APIENHANCED=/UD-Serv/API_Enhanced_City/

RUN apt-get install -y git

RUN git clone https://github.com/VCityTeam/UD-Serv.git

# RUN mkdir -p $APIENHANCED/api
WORKDIR $APIENHANCED

COPY .env .env
RUN pip install -r requirements.txt

# COPY . ./
ENV PYTHONPATH $APIENHANCED

CMD ["python", "api/web_api.py"]