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

### Notes
 * The clean-up work that MUST be done: refer to section "GGE said: demos to be realized/cleaned-up"
 * For the demos to be automatically restarted after a reboot of the Ubuntu VM
   inquire on e.g. 
   [this thread on docker-systemcl](https://www.ringingliberty.com/2020/09/16/systemctl-user-cannot-start-docker-containers-on-ubuntu-20-04/)
