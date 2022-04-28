This is a tutorial to reproduce two 3DTiles tilesets showed in the article.

## Installation

You can use either the Python application or the docker.

### Install Py3DTilers

Follow [installation steps](https://github.com/VCityTeam/py3dtilers#installation-from-sources) to install Py3DTilers

### Install the docker

Requires [Docker](https://docs.docker.com/get-docker/)

```bash
git clone https://github.com/VCityTeam/py3dtilers-docker
docker build -t vcity/py3dtilers Context
```

## 3D Tiles colored by height

Download the GeoJSON file available [here](https://raw.githubusercontent.com/VCityTeam/UD-Sample-data/master/GeoJSON/buildings_lyon1.geojson).

### With the application

Run the following command:

```bash
geojson-tiler --path path/to/buildings_lyon1.geojson --add_color HAUTEUR -o buildings_colored_by_height
```

The tileset will be created in a folder named `buildings_colored_by_height`

### With the docker

```bash
docker run --rm -t vcity/py3dtilers geojson-tiler --path path/to/buildings_lyon1.geojson --add_color HAUTEUR -o buildings_colored_by_height
```
