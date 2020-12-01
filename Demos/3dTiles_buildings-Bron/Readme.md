TODO CLEANUP: there is still a huge dependency towards rict and rict2
 * remove the [examples/DemoBron folder](https://github.com/VCityTeam/UD-Viz/tree/master/UD-Viz-Core/examples/DemoBron) from UD-Viz.
 * Remove Document browser (there is no datum specific to Bron!)
 * Remove the `3DTilesLayer.bron_building` and `servers.limonest_bron`
   variables from [UD-Viz-Core/examples/data/config/generalDemoConfig.json](https://github.com/VCityTeam/UD-Viz/blob/master/UD-Viz-Core/examples/data/config/generalDemoConfig.json) and deal with the consequences.
 * DemoBron/Demo.js: remove references to UD-Viz's generalDemoConfig.json
   (make a local copy, extract only what is bron related and plug that file)


A demo displaying 3dTiles of the building of the city of 
[Bron](https://en.wikipedia.org/wiki/Bron).

For installation (requires docker) run
```
./install.sh
docker-compose run -d
```
Use your we browser to open 
`http://localhost:8090/examples/DemoBron/Demo.html`

Halting the service is obtained with
```
docker-compose down
```.
