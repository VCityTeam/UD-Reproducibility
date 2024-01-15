# From Elaphes cave raw data to geolocalized 3DTiles

## Table of content
<!-- TOC -->

- [Table of content](#table-of-content)
- [Deriving the original data](#deriving-the-original-data)
  - [Initial download of the original data](#initial-download-of-the-original-data)
  - [Derive different formats out of the original data](#derive-different-formats-out-of-the-original-data)
  - [DTiles derivation of the original data](#dtiles-derivation-of-the-original-data)
- ["Sanitized" data and derived formats](#sanitized-data-and-derived-formats)
  - ["Sanitizing" the original data](#sanitizing-the-original-data)
  - [Offering different formats of the sanitized data](#offering-different-formats-of-the-sanitized-data)
  - [DTiles derivation of the sanitized data](#dtiles-derivation-of-the-sanitized-data)
- [Technical notes](#technical-notes)
  - [Concerning the geographical anchoring](#concerning-the-geographical-anchoring)
  - [Admin notes](#admin-notes)

<!-- /TOC -->

## Deriving the original data

### Initial download of the original data

The original `LAZ` raw data is hosted within the
[elaphes-cave LIRIS dataset](https://dataset-dl.liris.cnrs.fr/elaphes-cave/)
and more specifically in the 
https://dataset-dl.liris.cnrs.fr/elaphes-cave/Exp-Cloud-ELAPHS-94M.laz file.

Before downloading create a working directory to be used as sandbox for the
various derived files e.g. with

```bash
cd $(git rev-parse --show-cdup)/Computations/3DTiles/ElaphesCave
mkdir tmp
cd tmp
```

Then proceed with downloading the original
[`LAZ`](https://en.wikipedia.org/wiki/LAS_file_format#Compression) file
with e.g.
```bash
docker build -t ubuntu-wget DockerContexts/WgetContext
docker run -v `pwd`:/data ubuntu-wget wget --no-verbose https://dataset-dl.liris.cnrs.fr/elaphes-cave/Exp-Cloud-ELAPHS-94M.laz
```

### Derive different formats out of the original data

From [`LAZ`](https://en.wikipedia.org/wiki/LAS_file_format#Compression) to [`LAS`](https://en.wikipedia.org/wiki/LAS_file_format)
```bash
docker run -v `pwd`:/lastools hakonamdal/lastools las2las -i Exp-Cloud-ELAPHS-94M.laz -o Exp-Cloud-ELAPHS-94M.las
```

From  [`LAS`](https://en.wikipedia.org/wiki/LAS_file_format) to [`PLY`](https://en.wikipedia.org/wiki/PLY_(file_format))
```bash
docker run -v `pwd`:/data pdal/pdal pdal translate /data/Exp-Cloud-ELAPHS-94M.las /data/Exp-Cloud-ELAPHS-94M.ply
```

### 3DTiles derivation of the original data

Convert  [`LAZ`](https://en.wikipedia.org/wiki/LAS_file_format#Compression) format to [`3dTiles`](https://github.com/CesiumGS/3d-tiles) format
```bash
docker run -it --rm -v `pwd`:/data registry.gitlab.com/py3dtiles/py3dtiles:v7.0.0 convert /data/Exp-Cloud-ELAPHS-94M.laz --out /data/Exp-Cloud-ELAPHS-94M-3DTiles
```

Change the origin of the 3DTiles to "anchor" the tile-set the midst of 
[Lyon City](https://en.wikipedia.org/wiki/Lyon) 

```bash
docker build -t ubuntu-patch DockerContexts/PatchContext
docker run -it --rm -v `pwd`:/data ubuntu-patch /data/Exp-Cloud-ELAPHS-94M-3DTiles
```

## "Sanitized" data and derived formats

### "Sanitizing" the original data
<a name="anchor-sanitizing-the-original-data"></a>

The original 3D lasergrammetric data 
[Exp-Cloud-ELAPHS-94M.laz file](https://dataset-dl.liris.cnrs.fr/elaphes-cave/Exp-Cloud-ELAPHS-94M.laz)
has some (acquisition related?) artefacts: 
[three isolated points standing well aside from the rest of cave geometry](https://dataset-dl.liris.cnrs.fr/elaphes-cave/index.html#why-sanitize-and-what-was-sanitized).
Weeding out the three artifact points can be done with simple geometrical 
criteria with the help of the 
[`lastolas` LasTools utility](https://lastools.github.io/)
with the command
```bash
docker run -v `pwd`:/lastools hakonamdal/lastools las2las -i Exp-Cloud-ELAPHS-94M.laz -o Exp-Cloud-ELAPHS-94M-sanitized.laz -keep_z -10 10</code>
```

### Offering different formats of the sanitized data

```bash
docker run -it --rm -v `pwd`:/data registry.gitlab.com/py3dtiles/py3dtiles:v7.0.0 convert /data/Exp-Cloud-ELAPHS-94M-sanitized.laz --out /data/Exp-Cloud-ELAPHS-94M-sanitized.las
```


### 3DTiles derivation of the sanitized data

Convert [`LAZ`](https://en.wikipedia.org/wiki/LAS_file_format#Compression) format to [`3dTiles`](https://github.com/CesiumGS/3d-tiles) format

```bash
docker run -it --rm -v `pwd`:/data registry.gitlab.com/py3dtiles/py3dtiles:v7.0.0 convert /data/Exp-Cloud-ELAPHS-94M-sanitized.laz --out /data/Exp-Cloud-ELAPHS-94M-3DTiles-sanitized
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

### Admin notes

If your administrator role is to maintain the 
["elaphes-cave" LIRIS' dataset](https://dataset-dl.liris.cnrs.fr/elaphes-cave/)
you can cherry-pick among the following commands

Concerning the original data

```bash
scp Exp-Cloud-ELAPHS-94M.las connect:/dataset/elaphes-cave/
scp Exp-Cloud-ELAPHS-94M.ply connect:/dataset/elaphes-cave/
scp -r Exp-Cloud-ELAPHS-94M-3DTiles/ connect:/dataset/elaphes-cave/
```

Concerning the sanitized (derived) data
```bash
scp Exp-Cloud-ELAPHS-94M-sanitized.laz connect:/dataset/elaphes-cave/
scp Exp-Cloud-ELAPHS-94M-sanitized.las connect:/dataset/elaphes-cave/
scp Exp-Cloud-ELAPHS-94M-sanitized.ply connect:/dataset/elaphes-cave/
scp -r Exp-Cloud-ELAPHS-94M-sanitized-3DTiles/ connect:/dataset/elaphes-cave/
```