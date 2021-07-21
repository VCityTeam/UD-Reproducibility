# Geoserver setup docker

## General information

- IMPORTANT : This docker requires a [Geoserver](http://geoserver.org/) to run properly. You should have one currently installed and running, possibly in another docker or setup in your docker-compose for example. If you don't have one currently up and running, you can use this [docker](https://hub.docker.com/r/kartoza/geoserver/) to set one up.

This docker is used to upload data to your geoserver. It takes all the shapefile data stored in a directory and uploads it to the selected workspace of your geoserver. You can launch this docker simultaneously with your geoserver, and it will upload the data once the server is available. The Geoserver is mainly used to serve data not already available online (private data or data you have modified). The data you wish to upload on your geoserver should be uploaded in a git repository.

## How to use it

### Using docker-compose (recommended if you do not have a geoserver yet or if you want an easier deployment)

- Copy the context folder provided in this directory in your compose folder.
- Create a .env file in your compose folder (if one already exists, do not create another)
- Add the environment variables located in the "Geoserver-setup related section" located in [this file](Example/.env) to your own .env file.
- Configure the variables to suit your needs
- Build and launch your docker-compose.
- Access your geoserver, you should now be able to see the newly added layers.

### using docker (if you already havea geoserver installed)

Use the [Dockerfile](geoserver-setup-context/Dockerfile) provided within the geoserver-setup-context directory e.g. with
the following commands :
```
docker build geoserver-setup-context -t geoserver-setup 
--build-arg GEOSERVER_DATA_GITHUB_REPOSITORY=<Your_Github_Data_Repo>
--build-arg GEOSERVER_DATA_GITHUB_REPOSITORY_NAME=<Your_Github_Data_Repo_Name>
--build-arg GEOSERVER_DATA_IMPORT_DIR=<Your_Data_Path>

docker run --env-file ./Example/.env geoserver-setup
```

For the setup to function properly, you will need to configure several variables to access your geoserver.
Please refer to the [Geoserver setup section of the example .env file](./Example/.env) for the complete list of environment variables available and what they are used for.
To modify the content of these variables, you first need to modify the --build-arg variables content in the build command line. See the example below :
```
docker build geoserver-setup-context -t geoserver-setup 
--build-arg GEOSERVER_DATA_GITHUB_REPOSITORY=https://github.com/VCityTeam/UD-Reproducibility 
--build-arg GEOSERVER_DATA_GITHUB_REPOSITORY_NAME=UD-Reproducibility 
--build-arg GEOSERVER_DATA_IMPORT_DIR=Demos/DatAgora_PartDieu/data_import
```
See [this page](https://docs.docker.com/engine/reference/commandline/build/#set-build-time-variables---build-arg) for further instructions.

For all the other variables shown in the geoserver setup section, you can directly change their value in the .env file.

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
