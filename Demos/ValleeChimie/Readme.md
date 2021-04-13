A demo of 3DTiles based buildings accross [Lyon's chemistry valley](https://fr.wikipedia.org/wiki/Vall%C3%A9e_de_la_chimie).

## 1. Compute correct data for your demo
- Go on this folder [here](https://github.com/VCityTeam/UD-Reproducibility/tree/master/Computations/3DTiles/LyonTemporal/PythonCallingDocker)
- Edit the ``` demo_configuration.py``` configuration file in order to setup. For this demo we have compute cities in the Lyon's chemistry valley :

```
boroughs = [
           'FEYZIN',
           'GIVORS',
           'GRIGNY',
           'IRIGNY',
           'PIERRE_BENITE',
           'SOLAIZE',
           'LYON_7EME',
           'VERNAISON'
]
```
- Then follow this [instructions](https://github.com/VCityTeam/UD-Reproducibility/tree/master/Computations/3DTiles/LyonTemporal/PythonCallingDocker#readme)

## 2. Build ud-viz context

### 1. Configure your demo
- Go on the generaldemoConfig.json file in the ud-viz-contest folder
- (Optional) Change value of your extend position to visualize the correct map of your data, [here](https://github.com/VCityTeam/UD-Reproducibility/blob/master/Demos/ValleeChimie/ud-viz-context/generalDemoConfig.json#L44) :
- (Optional) To calculate this coordinates read this [doc](https://github.com/VCityTeam/VCity/wiki/Adapt_extent): 
 ```
   "extents": {
    "vallee_chimie": {
      "min_x": "1832891.32",
      "max_x": "1846735.29",
      "min_y": "5150253.55",
      "max_y": "5174952.52"
    }
  ```
- Place the correct url which aim on your data compute in the previous step, [here](https://github.com/VCityTeam/UD-Reproducibility/blob/master/Demos/ValleeChimie/ud-viz-context/generalDemoConfig.json#L61) :
```
  "3DTilesLayer":{
    "building":{
      "id":"3d-tiles-layer-building",
      "url":"http://rict2.liris.cnrs.fr/DataStore/ValleeChimie/tileset.json",
      "color": "0xFFFFFF",
      "initTilesManager": "true"
    }
 ```
### 2. Build your demo
 - Run this command line to build your context
```
docker build -t vallee-chimie ud-viz-context
```

- Retrieve your Fully Qualified Domain Name (FQDN):
   1. First retrieve your deploying host IP address. If ifconfig is
    available for you (Ubun tu, OSX) try using `ifconfig | grep -i inet`
   2. Then out of this IP adress retrieve the FQDN of your host with
    the `host <host_IP_number>` command.

- Then run the container with
```
docker run -d -h <FQDN> -p 8282:80/tcp -t vallee-chimie
```
- and open a web browser on URL http://localhost:8282/

