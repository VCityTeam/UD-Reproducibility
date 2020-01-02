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

## Demos: an Ubuntu based scafolding/deployment tool
```
Demos
└── Temporal-LyonMetropole
    ├── Components
    │   ├── Component1
    │   └── Component2
    ├── DockerComponent1.yml
    ├── DockerComponent2.yml
    ├── DockerCompose.yml
    ├── SomeSpecificConfiguration.html
    └── install.sh
```

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
