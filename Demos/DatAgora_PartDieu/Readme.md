A UD-Viz demo of 3DTiles based buildings and several urban data layers.
It was developed for a project about [the place of vegetation in cities](https://github.com/VCityTeam/DatAgora/wiki/Vegetalization-Project) by DatAgora

To setup your demo, you need to launch a terminal in this repository and run enter the following command :
```
docker-compose up
```
The setup will take several minutes. Once the geoserver is successfully launched and setup, you can try to connect to http://localhost:<PORT>/geoserver (<PORT> being the GEOSERVER_PORT configured in the .env file, 8080 by default)
The UD-viz page should also be accessible at http://localhost:<PORT> (<PORT> being this time the UD_VIZ_PORT configured in the .env file, 8999 by default)
