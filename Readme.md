# UD-Repoducibility general description
```
UD-Repoducibility
├── Articles
├── Computations
└── Demos
```

## Computations
The Computations sub-directory gathers the concrete means (scripts...) enabling the reproduction of of computations based on UD.

## Articles
The Articles sub-directory gathers the reproducibility oriented articles using the results of the computations (based on UD).

## Demos: an Ubuntu based scafolding/deployment tool (shell script version, to be deprecated soon)
The current directory holds a set of component oriented install shell scripts. 

Start by running the `sudo` dependent scripts
```
sudo ./install-packages.sh
sudo ./install-apache2.sh
```
You can assert that the http server is running by opening e.g. [http://rict2.liris.cnrs.fr/](http://rict2.liris.cnrs.fr/).

Then dependending on your needs you might run
```
./install-limonest-temporal.sh
```
Assert the result by opening e.g. [this temporal demo](http://rict2.liris.cnrs.fr/UD-Viz-Temporal-Limonest/UDV-Core/examples/DemoTemporal/Demo.html)

## Demos: a docker based deployment tool
The above shell-script way of doing things:
 - lacks modularity: all the demos share an http server or and UD-Viz component which doesn't accomodate to demos depending on conflicting versions such shared component (think of two versions)
 - impacts the considered hosts (in DEV or PROD) since it installs at the system level
 - can be quite cumbersome to deploy (even with the help of shell-scripts doing a part of the job)
 
We are thus moving to a docker compose deployment method
```
Demos
├── 3DTiles-Document-CityA-Demo
│   └── ...
└── Temporal-CityB-Demo
    ├── Component1            # E.g. UD-Viz
    │   ├── DockerContext
    │   │   ├── Dockerfile    # Pulling SHA1 designated versions of UD-Viz
    │   │   ├── Patches
    │   │   ├── SomeSpecificConfiguration.html
    │   │   └── ...
    │   ├── Docs
    │   └── docker-build.sh
    ├── Component2
    │   ├── DockerContext     # E.g. 3d-tiles-samples server
    │   ├── Data
    │   │   ├── pull-tileset-one.sh   # Pull from e.g. Zenodo
    │   │   └── recompute-tileset-two.sh
    │   └── docker-build.sh   # might call Data/pull-tileset-*.sh
    ├── DockerCompose.yml
    └── install.sh            # Might call Component[1|2]/docker-build.sh  
```

`install.sh` generaly endups with a `docker-compose up` and is launched with `nohup install.sh &`
 
**On going discussions**:
 - make sure [this topic meeting](https://github.com/VCityTeam/VCity/wiki/2019_12_20_VJA_EBO) content was taken into account
 - General logic: apply DRY over both `UD-Viz/../examples` and UD-Reproductibility/Demos
 - Three ways respect DRY
   * the [UD-Viz examples](https://github.com/VCityTeam/UD-Viz/tree/master/UD-Viz-Core/examples/DemoFull) data/server dependency is hardcoded towards some data server (think of rict2)
   * UD-Viz has no longer deployed examples. The UD-Viz standard demo acknowledges the fact that a standard demo is in fact the pair (UD-VIZ, UD-Serv) : in order to install such a demo we thus point to UD-reproducibility/Demos/Standard-demos that has the same status (tools, experession) as UD-reproducibility/Demos/Bron
   * the UD-Viz examples points to a configuration server (installed with UD-reproducibility) that dynamically lists the available data sets (bron, limonest, new-york_. In such a scenario note the dependency of the position of the camera (and possibly some menus like selecting the temporal GUI wdiget) towards the selected data : a demo is not only a data server but also a GUI configuration... 
