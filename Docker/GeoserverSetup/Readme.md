### Using docker-compose

    - IMPORTANT : This docker needs a geoserver to work properly. You should have one currently installed running, possibly in another docker or setup in your docker-compose

    - Copy the context folder provided in this directory in your compose folder.
    - Create a .env file in your compose folder (if one already exists, do not create another)
    - Add the following code to your .env file :
    ```
        # The directory holding the data to be imported in the geoserver
        GEOSERVER_DATA_IMPORT_DIR=data_import
        # The name of the workspace (geoserver notion) where the data should be uploaded. Make sure the selected workspace already exists on your geoserver.
        GEOSERVER_WORKSPACE=cite
        # The number of connection attempts that the setup should try to make prior to giving up (considering the geoserver failed)
        GEOSERVER_MAX_CONNECTION_ATTEMPTS=10
        # The wating delay (in number of seconds) in between two connection attempts
        GEOSERVER_TIME_CONNECTION_ATTEMPTS=5
        # The administrator username used for geoserver connection
        GEOSERVER_ADMIN_USER=admin
        # The associated admin password used for geoserver connection 
        GEOSERVER_ADMIN_PASSWORD=geoserver
    ```
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
