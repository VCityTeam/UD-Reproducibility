# Geoserver setup docker

## General information

- IMPORTANT : This docker requires a [Geoserver](http://geoserver.org/) to run properly. You should have one currently installed and running, possibly in another docker or setup in your docker-compose for example. If you don't have one currently up and running, you can use this [docker](https://hub.docker.com/r/kartoza/geoserver/) to set one up.

This docker is used to upload data to your geoserver. It takes all the shapefile data stored in a directory and uploads it to the selected workspace of your geoserver. You can launch this docker simultaneously with your geoserver, and it will upload the data once the server is available.

## How to use it

### using docker

### Using docker-compose


- Copy the context folder provided in this directory in your compose folder.
- Create a .env file in your compose folder (if one already exists, do not create another)
- Add the environment variables located in the "Geoserver-setup related section" located in [this file](Example/.env) to your own .env file.
- Configure the variables to suit your needs
- Build and launch your docker-compose.
- Access your geoserver, you should now be able to see the newly added layers.

## Developers

### Linting the python source
In order to apply the coding style
```
$ virtualenv -p python3 venv
$ source venv/bin/activate
(venv) pip install -r requirements.tx
```
The manual application of pylint is done with
```
(venv) pylint python_setup.py
```

### For direnv users
```
ln -s .envrc.tpl .envrc
$ direnv allow
(venv)
```
