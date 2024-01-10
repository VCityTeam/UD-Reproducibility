# From Elaphes cave raw data to geolocalized 3DTiles

The original `LAZ` raw data is hosted within the
[elaphes-cave LIRIS dataset](https://dataset-dl.liris.cnrs.fr/elaphes-cave/)
and more specifically in the 
https://dataset-dl.liris.cnrs.fr/elaphes-cave/Exp-Cloud-ELAPHS-94M.laz file.

The computing pipeline then goes

```bash
cd $(git rev-parse --show-cdup)/Computations/3DTiles/ElaphesCave
mkdir work
cd tmp
```

Download the original `LAZ` file
```bash
docker build -t ubuntu-wget DockerContexts/WgetContext
docker run -v `pwd`:/data ubuntu-wget wget --no-verbose https://dataset-dl.liris.cnrs.fr/elaphes-cave/Exp-Cloud-ELAPHS-94M.laz
```

Convert `LAZ` format to `3dTiles` format
```bash
docker run -it --rm -v `pwd`:/data registry.gitlab.com/py3dtiles/py3dtiles:v7.0.0 convert /data/Exp-Cloud-ELAPHS-94M.laz --out /data/Exp-Cloud-ELAPHS-94M-3DTiles
```

Change the origin of the 3DTiles to "anchor" the tile-set the midst of 
[Lyon City](https://en.wikipedia.org/wiki/Lyon) 

```bash
docker build -t ubuntu-patch DockerContexts/PatchContext
docker run -it --rm -v `pwd`:/data ubuntu-patch /data/Exp-Cloud-ELAPHS-94M-3DTiles
```

## Technical notes

### Concerning the geographical anchoring

If one tries to offset the upstream `LAZ` file with the `lastolas` utility e.g.
with the command

```bash
docker run -v `pwd`:/lastools hakonamdal/lastools las2las -reoffset 1842455.8752944241 5174639.096373817 201 -i Exp-Cloud-ELAPHS-94M.laz -o Exp-Cloud-ELAPHS-94M-offseted_to_lyon.laz
```

then one gets

```
WARNING: reoffsetting from 31.8927 to 1.84128e+006 causes LAS integer overflow for min_x
```

Although `py3Dtilers` offerts to re-offset tilesets (by using the 
transformation matrix) this tool can _only_ be used for 3DTiles that wrap 
`b3dm` data as opposed to `.pnts` data (point cloud). We thus cannot use it
in this context.