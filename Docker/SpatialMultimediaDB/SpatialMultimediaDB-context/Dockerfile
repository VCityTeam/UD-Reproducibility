FROM python:3.6

LABEL maintainer "VCityTeam"
LABEL source.repo "https://github.com/VCityTeam/UD-Serv.git"

ARG ordbms
ENV ordbms=${ordbms}
ARG user
ENV user=${user}
ARG password
ENV password=${password}
ARG host
ENV host=${host}
ARG port
ENV port=${port}
ARG dbname
ENV dbname=${dbname}

RUN apt-get update

ARG APIENHANCED=/UD-Serv/API_Enhanced_City/

RUN apt-get install -y git

RUN git clone https://github.com/VCityTeam/UD-Serv.git

RUN echo "ordbms=${ordbms}\nuser=${user}\npassword=${password}\nhost=${host}\nport=${port}\ndbname=${dbname}" > $APIENHANCED.env

WORKDIR $APIENHANCED

RUN pip install -r requirements.txt

ENV PYTHONPATH $APIENHANCED

CMD ["python", "api/web_api.py"]