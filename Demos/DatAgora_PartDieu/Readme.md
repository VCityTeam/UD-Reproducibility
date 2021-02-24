A UD-Viz demo of 3DTiles based buildings and several urban data layers.
It was developed for a project about [the place of vegetation in cities](https://github.com/VCityTeam/DatAgora/wiki/Vegetalization-Project) by DatAgora

To setup your demo, you need to launch a terminal in this repository and run enter the following command :
```
docker-compose up
```
The setup will take several minutes. Once the geoserver is successfully launched and setup, you can try to connect to http://localhost:8080/geoserver (8080 being the GEOSERVER_PORT configured in the .env file, set to 8080 by default)
The UD-viz page should also be accessible at http://localhost:8999 (8999 being this time the UD_VIZ_PORT configured in the .env file, 8999 by default)

There are several variables you can customize in the .env file if needed :


 * GEOSERVER_PORT : the port used to access the geoserver (8080 by default)
 * GEOSERVER_ADMIN_USER : the admin username used to connect to the geoserver ("admin" by default)
 * GEOSERVER_ADMIN_PASSWORD : the admin password used to connect to the geoserver ("geoserver" by default)

 * GEOSERVER_MAX_CONNECTION_ATTEMPTS : number of attempts to try and connect to the geoserver for the setup container (10 by default)
 * GEOSERVER_TIME_CONNECTION_ATTEMPTS : number of seconds to between connection attempts to the geoserver for the setup container (5 by default)

 * UD_VIZ_PORT :  the port used to access the ud-viz demo (8999 by default)
