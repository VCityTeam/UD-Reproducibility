# References
# - on chosing your Python base container
#   https://pythonspeed.com/articles/base-image-python-docker-images/
#   https://stackoverflow.com/questions/52740556/python-3-7-docker-images

FROM python:3.7-buster

COPY city_gml_files_from_archive.py ./
COPY demo_lyon_metropole_dowload_and_sanitize.py ./
COPY demo_lyon_metropole_dowload_and_sanitize_static.py ./
COPY demo_static.py ./
COPY demo.py ./
COPY entrypoint.py ./
COPY pushd.py ./

COPY requirements.txt ./
RUN pip3 install -r requirements.txt

CMD ["python3", "./entrypoint.py"]