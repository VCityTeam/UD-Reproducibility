FROM cesium-gs/3d-tiles-samples

RUN apt-get update
RUN apt-get install -y wget

# Import an example of 3DTiles embedding some IFC geometry
RUN cd tilesets/ && \
    wget --recursive --no-parent -nH --cut-dirs=1 --reject="index.html*" \
       http://rict2.liris.cnrs.fr/DataStore/bron_tiles/
