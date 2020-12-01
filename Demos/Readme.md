This directory gathers docker based deployment tools for the demos.
The general sub-directory structure is as follows:
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

Historical note: refer to the [old shell-script way of things](Oldies/Readme.md) for
design reasons on using docker.
