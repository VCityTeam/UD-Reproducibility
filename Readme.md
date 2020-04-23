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
 - **General logic**: 
    * The notion of "Usage Context" (UC) of UD-Viz: using UD-Viz de facto requires
       - a set of modules, 
       - a set of data servers,
       - a scene description (position of the camera, pre-selected objects...)
    * There are many Usage Contexts (corresponding to demos) e.g. Bron-temporel, Lyon-Villeurbane-Doc_module.
    * There are two types of UD-Viz Usage Contexts:
       - the ones that can default the server side to some canonical data server set (think of rict2): for example
          * the standard UD-Viz demo (Usage Context) for which the user wishing to install and try out the UD-Viz client side can accept to use some pre-installed (VCityTeam managed) remote data servers
          * a UD-Viz client side developer that can also accept such a dependency towards pre-installed remote data servers
          * a module specific UDV-Viz demo
       - the ones requiring the installation of some set of data servers (in order to develop the server side or to install rict2 itself)<br>
    * Adopted principle: a considered UC should have an implementation for each of the above categories. For example the Demo-Bron UC should exist 
       1. within the UD-Viz repositor and using the canonical data server (think of rict2)
       2. within `UD-Reproductibility/Demos` where it re-deploys the data server set and pactches the scene description to point to the newly installed data servers (as opposed to the canonical ones).
 - **Data related good practice**: place all demo data on a [zenodo](https://zenodo.org/) like site and have the UD-Reproductibility demo pull them (note that Zenod allows for 50G maximum per data repository, and no number of repository limite)
- Related actions (belongin to an issue)
    * the UD-Viz [FullDemo](https://github.com/VCityTeam/UD-Viz/tree/master/UD-Viz-Core/examples/DemoFull) demo might be renamed AllModulesDemo
    * the UD-Viz [DemoStable/](https://github.com/VCityTeam/UD-Viz/tree/master/UD-Viz-Core/examples/DemoFull) demo should be renamed LyonDocuments (and corresponds to the FabPat project)
    * [DemoWindow](https://github.com/VCityTeam/UD-Viz/tree/master/UD-Viz-Core/examples/DemoWindow) that technically illustrate some `Utils` feature (as opposed to a module) and that should be moved to [UD-Viz/UD-Viz-Core/src/Utils/GUI/examples](https://github.com/VCityTeam/UD-Viz/tree/master/UD-Viz-Core/src/Utils/GUI/) (the examples sub-directory having to be created)
    * All the UD-Viz UCs must be cloned and adapted for their data server side to `UD-Reproductibility/Demos`
    * Update the [main index.html descritpion](https://github.com/VCityTeam/UD-Viz/blob/master/UD-Viz-Core/index.html) and provide an UC oriented description (module, data, scene descritpion) of what each demo is
      - [UD-Viz/DemoBron](https://github.com/VCityTeam/UD-Viz/tree/master/UD-Viz-Core/examples/DemoBron): make a description of what Bron is and what data is used... 
      - [UD-Viz/DemoLimonest](https://github.com/VCityTeam/UD-Viz/tree/master/UD-Viz-Core/examples/DemoLimonest): ditto mutatis mutandis.
      - [UD-Viz/DemoMultiLayer](https://github.com/VCityTeam/UD-Viz/tree/master/UD-Viz-Core/examples/DemoMultiLayer): just a specific 3dTiles), 
      - [UD-Viz/DemoPC](https://github.com/VCityTeam/UD-Viz/tree/master/UD-Viz-Core/examples/DemoPC): which specific Point Cloud set is this about, 
      - [UD-Viz/DemoStable](https://github.com/VCityTeam/UD-Viz/tree/master/UD-Viz-Core/examples/DemoStable): a subset of modules, together with specific data server e.g. Lyon documents: this demo was called stable to illustrate enhanced data servers) to `UD-Reproductibility/Demos` 
   * make a [`MAM` tag](https://github.com/VCityTeam/UD-Viz/tags) of the current version and remove the [UD-Viz/UD-Viz-Core/examples/MAM](https://github.com/VCityTeam/UD-Viz/tree/master/UD-Viz-Core/examples/MAM) directory that is not up-todate.
   * Once temporal related code gets moved to the UD-Viz master create the UD-Viz version of the [Temporal-LyonMetropole](https://github.com/VCityTeam/UD-Reproducibility/tree/master/Demos/Temporal-LyonMetropole) UD-Reproductibility UC.


