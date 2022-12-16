This is a tutorial to reproduce two 3DTiles tilesets showed in the article.

## Installation

You can use either the Python application or the docker of Py3DTilers.

### Install the application

Follow [installation steps](https://github.com/VCityTeam/py3dtilers#installation-from-sources) to install Py3DTilers.

### Install the docker

Requires [Docker](https://docs.docker.com/get-docker/)

```bash
git clone https://github.com/VCityTeam/py3dtilers-docker
cd py3dtilers-docker
docker build -t vcity/py3dtilers Context
```

## 3D Tiles colored by height

Download the GeoJSON file available [here](https://raw.githubusercontent.com/VCityTeam/UD-Sample-data/master/GeoJSON/buildings_lyon1.geojson).

### With the application

Run the following command:

```bash
geojson-tiler --path <path/to>/buildings_lyon1.geojson --add_color HAUTEUR -o buildings_colored_by_height
```

Where `<path/to>` is the relative or absolute path to the folder containing the GeoJSON file.

The tileset will be created in the root directory of the application in a folder named `buildings_colored_by_height`.

### With the docker

```bash
docker run --rm -v <absolute/path/to/folder>:/mnt/data/ -t vcity/py3dtilers geojson-tiler --path /mnt/data/buildings_lyon1.geojson --add_color HAUTEUR -o /mnt/data/buildings_colored_by_height
```

Where `<absolute/path/to/folder>` is the __absolute path__ to the folder containing the GeoJSON file.

The tileset will be created in a folder named `<absolute/path/to/folder>/buildings_colored_by_height`.

## Visualise the 3D Tiles

If you want to visualise 3D Tiles tilesets, refer to [this tutorial](https://github.com/VCityTeam/UD-SV/blob/master/ImplementationKnowHow/Visualize3DTiles.md) 
