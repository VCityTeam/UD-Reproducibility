
A demo of 3DTiles based buildings accross [Lyon's chemistry valley](https://fr.wikipedia.org/wiki/Vall%C3%A9e_de_la_chimie).

## 1. Compute correct data for your demo
Note: this process is on the [verge of being dockerized](../../Computations/3DTiles/ChemistryValley)

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
           'ST_FONS',
           'LYON_7EME',
           'VERNAISON'
]
```
- Then follow this [instructions](https://github.com/VCityTeam/UD-Reproducibility/tree/master/Computations/3DTiles/LyonTemporal/PythonCallingDocker#readme)

## 2. Build ud-viz context

### 2.1 Configure your demo
- Go on the [config.json file](https://github.com/VCityTeam/UD-Viz-Template/blob/master/assets/config/config.json) to configure the location of your data and the set the 3D tiles path.

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
- Place the correct url which aim on your data compute in the previous step, [here](https://github.com/VCityTeam/UD-Reproducibility/blob/master/Demos/ValleeChimie/ud-viz-context/ChemistryValley/assets/config/config.json#L67) :
```
  "3DTilesLayer":{
    "building":{
      "id":"3d-tiles-layer-building",
      "url":"http://rict2.liris.cnrs.fr/DataStore/ValleeChimie/tileset.json",
      "color": "0xFFFFFF",
      "initTilesManager": "true"
    }
 ```
### 2.2 Build your demo
 - Run this command line to build your context
```
- docker-compose build
- docker-compose up
```

- and open a web browser on URL http://localhost:8999/

