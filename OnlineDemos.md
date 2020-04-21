## Technical/admin elements on [public online demos](https://github.com/MEPP-team/UD-SV/blob/master/UD-Doc/OnlineDemos.md) and [private online demos](#private-demos)

### [Public demos](https://github.com/MEPP-team/UD-SV/blob/master/UD-Doc/OnlineDemos.md) on rict
  * [UD-Viz Demos](http://rict.liris.cnrs.fr/UDVDemo/UDV/UDV-Core/) (front-end)
    * Although the following sub-demos (of this section) distinguish themselves from one another by the usage of specific directories (or sub-servers?), they do share 
       - some GrandLyon data servers
       - the Tileset server
       - others ?
    * [Stable demo](http://rict.liris.cnrs.fr/UDVDemo/UDV/UDV-Core/examples/DemoStable/Demo.html): 
      * [Public description](https://github.com/MEPP-team/UD-SV/blob/master/UD-Doc/OnlineDemos.md#demo-online-UD-Viz-stable-end-user-modules)
      * Backend: EnhancedCity DB / API on rict.liris.cnrs.fr in `Demos/UDVDemo/UDV-server-stable/API_Enhanced_City`. It is visible from the outside on port 443 and it can be started with `sudo docker-compose up`.
    * [Full modules demo](http://rict.liris.cnrs.fr/UDV-stable/UDV/UDV-Core/examples/DemoFull/Demo.html): 
      * [Public description](https://github.com/MEPP-team/UD-SV/blob/master/UD-Doc/OnlineDemos.md#demo-online-UD-Viz-full-modules)
      * Backend: EnhancedCity DB / API on rict.liris.cnrs.fr in `Demos/UDVDemo/UDV-server-dev/API_Enhanced_City`. It is visible from the outside on port 1525 and it can be started with `sudo docker-compose up`.
    * Admin account (used within the demo, refer to the bottom "sign in" button, in order to create/delete authenticated users): 
      * username: `admin`
      * password: `Hello Rict 2019 !` (words are separated by spaces, no trailing space).
      * Full modules demo: 
    * Restarting the front end after a shutdown or an update of UDV: one needs to do `npm install` and `npm run build`. This last step will create the udvcore bundle. Note that this bundle is automatically created by `npm start`; however here we do not use npm to serve the client code which is served by Apache. Hence we must execute this command manually.

  * [City wide 3dTiles tileset visualization](http://rict.liris.cnrs.fr/Demo_LyonFull_Villeurbanne_Bron_2015/UDV/UDV-Core/examples/DemoFull/Demo.html):
     * Status: [public](https://github.com/MEPP-team/UD-SV/new/master/UD-Doc/OnlineDemos.md#demo-online-3dtiles-lyon-villeurbanne)

  * [3DTiles at the city level with 3 timestamps](http://rict.liris.cnrs.fr/iTownsPlanar3DTiles/itowns/examples/planar_3dtiles.html)

     * This demo is currently in a [PR acceptance process in iTowns](https://github.com/iTowns/itowns/pull/1034) 
     * After a shutdown; this demo re-starts alone as everything is served using Apache which is automatically restarted when the VM is reboot

### Public demos on rict2
Offered demos:
 - [Rict2 gateway](http://rict2.liris.cnrs.fr/)
 - [DemoLimonest](http://rict2.liris.cnrs.fr/UD-Viz/UD-Viz-Core/examples/DemoLimonest/Demo.html) 
 - [DemoBron](http://rict2.liris.cnrs.fr/UD-Viz/UD-Viz-Core/examples/DemoBron/Demo.html)
 - [Temporal-Limonest](http://rict2.liris.cnrs.fr/UD-Viz-Temporal-Limonest/UDV-Core/examples/DemoTemporal/Demo.html): requires pointing the camera to Limonest AND activate the temporal GUI gizmo
 - [Temporal-Bron](http://rict2.liris.cnrs.fr/UD-Viz-Temporal-Limonest/UDV-Core/examples/DemoTemporalBron/Demo.html): : requires pointing the camera to Bron AND activate the temporal GUI gizmo

**Installation notes**:<br>
Apache2 server: refer to /etc/apache2/sites-enabled/rict2.liris.cnrs.fr.conf that serves the directory
`DocumentRoot /home/citydb_user/UD-Deploy/WebDemos` that in turn has three sub-directories
  * [Datastore](http://rict2.liris.cnrs.fr/Datastore`) that holds tiles
  * [UD-Viz-Temporal-Limonest/](http://rict2.liris.cnrs.fr/UD-Viz-Temporal-Limonest/)
  * [http://rict2.liris.cnrs.fr/UD-Viz/UD-Viz-Core/](http://rict2.liris.cnrs.fr/UD-Viz/UD-Viz-Core/) that offers
      - [DemoLimonest](http://rict2.liris.cnrs.fr/UD-Viz/UD-Viz-Core/examples/DemoLimonest/Demo.html) corresponding to [this repository entry](https://github.com/VCityTeam/UD-Viz/tree/master/UD-Viz-Core/examples/DemoLimonest)
      - [DemoBron](http://rict2.liris.cnrs.fr/UD-Viz/UD-Viz-Core/examples/DemoBron/Demo.html) corresponding to [this repository entry](https://github.com/VCityTeam/UD-Viz/tree/master/UD-Viz-Core/examples/DemoBron)
  * [http://rict2.liris.cnrs.fr/UD-Viz-Temporal-Limonest](http://rict2.liris.cnrs.fr/UD-Viz-Temporal-Limonest) that offers
      - [DemoLimonest](http://rict2.liris.cnrs.fr/UD-Viz-Temporal-Limonest/UDV-Core/examples/DemoTemporal/Demo.html): WARNING the corresponding configuration files (`data/config/generalDemoConfig.json` and  `../src/Utils/BaseDemo/js/BaseDemo.js` within ``UD-Deploy/WebDemos/UD-Viz-Temporal-Limonest/UDV-Core/examples`) were NOT PUSHED on git 
      - [DemoBron](UD-Viz-Temporal-Limonest/UDV-Core/examples/DemoTemporalBron/Demo.html): WARNING the corresponding directory (`UD-Deploy/WebDemos/UD-Viz-Temporal-Limonest/UDV-Core/examples/DemoTemporalBron`) was NOT PUSHED on git 

### Private demos<a name="private-demos"></a>
  * [Vilo3d](http://rict.liris.cnrs.fr/Vilo3D/UDV/Vilo3D/index.html)
     * Working with a freezed (and tagged) [version of UDV](https://github.com/MEPP-team/UDV/tree/Vilo3D-Demo-1.0) last modified on the Sep 12, 2017.  
     * Restarting Vilo3D building server service on rict.liris.cnrs.fr after a shutdown:
       ```
       cd Demos/Vilo3D/building-server.git
       source venv/bin/activate
       ./venv/bin/uwsgi --yml conf/building.uwsgi.yml --http-socket :1521 &
       ```
