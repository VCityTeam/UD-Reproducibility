# From Elaphes cave raw data to geolocalized 3DTiles

The original `LAZ` raw data is hosted within the
[elaphes-cave LIRIS dataset](https://dataset-dl.liris.cnrs.fr/elaphes-cave/)
and more specifically in the 
https://dataset-dl.liris.cnrs.fr/elaphes-cave/Exp-Cloud-ELAPHS-94M.laz file.

The computing pipeline then goes

```bash
cd $(git rev-parse --show-cdup)/Computations/3DTiles/ElaphesCave
docker build -t ubuntu-wget DockerContexts/WgetContext
docker build -t ubuntu-patch DockerContexts/PatchContext

mkdir work
cd tmp

# Download original LAZ file
docker run -v `pwd`:/data ubuntu-wget wget --no-verbose https://dataset-dl.liris.cnrs.fr/elaphes-cave/Exp-Cloud-ELAPHS-94M.laz

# Convert LAZ to 3dTiles
docker run -it --rm -v `pwd`:/data registry.gitlab.com/py3dtiles/py3dtiles:v7.0.0 convert /data/Exp-Cloud-ELAPHS-94M.laz --out /data/Exp-Cloud-ELAPHS-94M-3DTiles

# Change the origin of the 3DTiles to become the midst of Lyon City
docker run -it --rm -v `pwd`:/data ubuntu-patch /data/Exp-Cloud-ELAPHS-94M-3DTiles
```