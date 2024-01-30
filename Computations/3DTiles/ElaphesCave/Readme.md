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
- [UNDER CONSTRUCTION](#under-construction)

<!-- /TOC -->

## Deriving the original data

### Initial download of the original data

The original [`LAZ`](https://en.wikipedia.org/wiki/LAS_file_format#Compression)
raw data is hosted within the
[elaphes-cave LIRIS dataset](https://dataset-dl.liris.cnrs.fr/elaphes-cave/)
and more specifically in the 
https://dataset-dl.liris.cnrs.fr/elaphes-cave/Exp-Cloud-ELAPHS-94M.laz file.

In order to simplify scripting, create the `ELAPHE_DIR` environment variable
```bash
export ELAPHE_DIR=`cd $(git rev-parse --show-cdup)/Computations/3DTiles/ElaphesCave ; pwd -P`
```

Create a data sandbox, and initialize it by downloading the original
[`LAZ`](https://en.wikipedia.org/wiki/LAS_file_format#Compression) file
with e.g.

```bash
cd $ELAPHE_DIR
mkdir data
docker build -t ubuntu-wget DockerContexts/WgetContext
docker run -v `pwd`/data:/data ubuntu-wget wget --no-verbose https://dataset-dl.liris.cnrs.fr/elaphes-cave/Exp-Cloud-ELAPHS-94M.laz
```

### Derive different formats out of the original data

From [`LAZ`](https://en.wikipedia.org/wiki/LAS_file_format#Compression) to [`LAS`](https://en.wikipedia.org/wiki/LAS_file_format)
```bash
cd $ELAPHE_DIR
docker run -v `pwd`/data:/lastools hakonamdal/lastools las2las -i Exp-Cloud-ELAPHS-94M.laz -o Exp-Cloud-ELAPHS-94M.las
```

From  [`LAS`](https://en.wikipedia.org/wiki/LAS_file_format) to [`PLY`](https://en.wikipedia.org/wiki/PLY_(file_format))
```bash
cd $ELAPHE_DIR
docker run -v `pwd`/data:/data pdal/pdal pdal translate /data/Exp-Cloud-ELAPHS-94M.las /data/Exp-Cloud-ELAPHS-94M.ply
```

### 3DTiles derivation of the original data

Convert  [`LAZ`](https://en.wikipedia.org/wiki/LAS_file_format#Compression) format to [`3dTiles`](https://github.com/CesiumGS/3d-tiles) format
```bash
cd $ELAPHE_DIR
docker run -it --rm -v `pwd`/data:/data registry.gitlab.com/py3dtiles/py3dtiles:v7.0.0 convert /data/Exp-Cloud-ELAPHS-94M.laz --out /data/Exp-Cloud-ELAPHS-94M-3DTiles
```

Provide 3DTiles [tile-set "anchor"](#concerning-the-geographical-anchoring) in
the midst of 
[Lyon City](https://en.wikipedia.org/wiki/Lyon) 

```bash
cd $ELAPHE_DIR
docker build -t ubuntu-patch DockerContexts/PatchContext
docker run -it --rm -v `pwd`/data:/data ubuntu-patch /data/Exp-Cloud-ELAPHS-94M-3DTiles/tileset.json
```
which should create a new `tileset-lyon_offset.json` file in the same directory
as the original `tileset.json`.

## "Sanitized" data and derived formats

### "Sanitizing" the original data
<a name="anchor-sanitizing-the-original-data"></a>

The original 3D lasergrammetric data 
[Exp-Cloud-ELAPHS-94M.laz file](https://dataset-dl.liris.cnrs.fr/elaphes-cave/Exp-Cloud-ELAPHS-94M.laz)
has some (acquisition related?) artefacts: 
[three isolated points standing well aside from the rest of cave geometry](https://dataset-dl.liris.cnrs.fr/elaphes-cave/index.html#anchor-why-sanitize-and-what-was-sanitized).
Weeding out the three artifact points can be done with simple geometrical 
criteria with the help of the 
[`lastolas` LasTools utility](https://lastools.github.io/)
with the command

```bash
cd $ELAPHE_DIR
docker run -v `pwd`/data:/lastools hakonamdal/lastools las2las -i Exp-Cloud-ELAPHS-94M.laz -o Exp-Cloud-ELAPHS-94M-sanitized.laz -keep_z -10 10
```

### Offering different formats of the sanitized data

From [`LAZ`](https://en.wikipedia.org/wiki/LAS_file_format#Compression) to [`LAS`](https://en.wikipedia.org/wiki/LAS_file_format)
```bash
cd $ELAPHE_DIR
docker run -v `pwd`/data:/lastools hakonamdal/lastools las2las -i Exp-Cloud-ELAPHS-94M-sanitized.laz -o Exp-Cloud-ELAPHS-94M-sanitized.las
```

From  [`LAS`](https://en.wikipedia.org/wiki/LAS_file_format) to [`PLY`](https://en.wikipedia.org/wiki/PLY_(file_format))
```bash
cd $ELAPHE_DIR
docker run -it --rm -v `pwd`/data:/data pdal/pdal pdal translate /data/Exp-Cloud-ELAPHS-94M-sanitized.las /data/Exp-Cloud-ELAPHS-94M-sanitized.ply
```
  
### 3DTiles derivation of the sanitized data

Convert [`LAZ`](https://en.wikipedia.org/wiki/LAS_file_format#Compression) format to [`3dTiles`](https://github.com/CesiumGS/3d-tiles) format

```bash
cd $ELAPHE_DIR
docker run -it --rm -v `pwd`/data:/data registry.gitlab.com/py3dtiles/py3dtiles:v7.0.0 convert /data/Exp-Cloud-ELAPHS-94M-sanitized.laz --out /data/Exp-Cloud-ELAPHS-94M-sanitized-3DTiles
```

Provide 3DTiles [tile-set "anchor"](#concerning-the-geographical-anchoring) in
the midst of 
[Lyon City](https://en.wikipedia.org/wiki/Lyon) 

```bash
cd $ELAPHE_DIR
docker build -t ubuntu-patch DockerContexts/PatchContext
docker run -it --rm -v `pwd`/data:/data ubuntu-patch /data/Exp-Cloud-ELAPHS-94M-sanitized-3DTiles/tileset.json
```
which should create a new `tileset-lyon_offset.json` file in the same directory
as the original `tileset.json`.

## Technical notes

### Concerning the geographical anchoring

If one tries to offset the upstream `LAZ` file with the `lastolas` utility e.g.
with the command

```bash
cd $ELAPHE_DIR
docker run -v `pwd`/data:/lastools hakonamdal/lastools las2las -reoffset 1842455.8752944241 5174639.096373817 201 -i Exp-Cloud-ELAPHS-94M.laz -o Exp-Cloud-ELAPHS-94M-offseted_to_lyon.laz
```

then one gets

```
WARNING: reoffsetting from 31.8927 to 1.84128e+006 causes LAS integer overflow for min_x
```

Although `py3Dtilers` offerts to re-offset tilesets (by using the 
transformation matrix) this tool can _only_ be used for 3DTiles that wrap 
`b3dm` data as opposed to `.pnts` data (point cloud). We thus cannot use it
in this context.

## Admin notes

If your administrator role is to maintain the 
["elaphes-cave" LIRIS' dataset](https://dataset-dl.liris.cnrs.fr/elaphes-cave/)
you can cherry-pick among the following commands

Concerning the original data

```bash
# The original laz file was sourced in
scp Exp-Cloud-ELAPHS-94M.las connect:/dataset/elaphes-cave/
scp Exp-Cloud-ELAPHS-94M.ply connect:/dataset/elaphes-cave/
scp -r Exp-Cloud-ELAPHS-94M-3DTiles/ connect:/dataset/elaphes-cave/
scp -r Exp-Cloud-ELAPHS-94M-3DTiles/tileset-lyon_offset.json connect:/dataset/elaphes-cave/Exp-Cloud-ELAPHS-94M-3DTiles/
```

Concerning the sanitized (derived) data
```bash
scp Exp-Cloud-ELAPHS-94M-sanitized.laz connect:/dataset/elaphes-cave/
scp Exp-Cloud-ELAPHS-94M-sanitized.las connect:/dataset/elaphes-cave/
scp Exp-Cloud-ELAPHS-94M-sanitized.ply connect:/dataset/elaphes-cave/
scp -r Exp-Cloud-ELAPHS-94M-sanitized-3DTiles/ connect:/dataset/elaphes-cave/
scp -r Exp-Cloud-ELAPHS-94M-sanitized-3DTiles/tileset-lyon_offset.json connect:/dataset/elaphes-cave/Exp-Cloud-ELAPHS-94M-sanitized-3DTiles/tileset-lyon_offset.json
scp Exp-Cloud-ELAPHS-94M-sanitized-just-normals-with-CloudCompare.pts connect:/dataset/elaphes-cave/
```


## UNDER CONSTRUCTION
From [`LAZ`](https://en.wikipedia.org/wiki/LAS_file_format#Compression) to 
[`PTS-with-normals](https://paulbourke.net/dataformats/pts/).
Alas this process is a manual one and is realized with CloudCompare (version at
least 2.12.3 in order for the PCL-wrapper plugin to be available).
The process goes:
* Fire CloudCompare and import Exp-Cloud-ELAPHS-94M.laz
* Plugins (menu) ---> PCL wrapper ---> Estimate Normals and Curvature
* Popup menu: toggle on "use Knn search" and leave the default argument 
  value of `10` (disregard the curvature toggle that we won't use anyhow),
  and launch the computation with the `OK` button.
* Once the normal computations are realized, export the result to an ASC or
  PTS file (that are only distinguished by the presence/absence of some
  attributes like intensity, curvature, vertex colors as well as their 
  relative). For this
  <br> 
  File (menu) save ---> Select ASCII cloud as format ---> 
  Provide e.g. `Exp-Cloud-ELAPHS-94M-sanitized-normals-with-CloudCompare.asc` 
  as filename for exportation ---> `OK` button
* Sub-menu: select `10` for coordinate precision, `8` as scalar precision,
  toggle on both of header options (columns title and number of points),
  disregard the colors options (since DGtal doesn't know how to use them)
  and eventually hit `OK` button.
* Because DGTal:pc2vol requires a `.pts` formatted input that is strictly 
  limited to columns `X, Y, Z, Nz, ny, Nz` (that is position and normal),
  remove the two header lines (that we kept for the record) and remove the
  unwanted attribute columns with 
  ```bash
  tail -n +2 Exp-Cloud-ELAPHS-94M-sanitized-normals-with-CloudCompare.pts | cut -d\  -f1,2,3,9,10,11 > Exp-Cloud-ELAPHS-94M-sanitized-just-normals-with-CloudCompare.pts
  ```
* Optionally remove the intermediate files with
  ```bash
  rm Exp-Cloud-ELAPHS-94M-sanitized-normals-with-CloudCompare.asc
  rm Exp-Cloud-ELAPHS-94M-sanitized-normals-with-CloudCompare.pts
  ```
* Notes: there is some hope for dockerizing the above process
  - on OSX
    ```bash
    /Applications/CloudCompare.app/Contents/MacOS/CloudCompare -SILENT -O Exp-Cloud-ELAPHS-94M-sanitized.laz -OCTREE_NORMALS 10 -C_EXPORT_FMT ASC -SAVE_CLOUDS -PREC 10 -SEP SPACE
    ```
    References:
    * https://www.cloudcompare.org/doc/wiki/index.php?title=Command_line_mode
    * https://stackoverflow.com/questions/76129221/automated-way-to-convert-point-clouds-from-asc-to-ply-format-and-compute-norma
  - CloudCompare dockers:
    * https://github.com/dockerstuff/docker-cloudcompare
    * https://hub.docker.com/r/saracen9/cloudcompare#!
    * https://github.com/tyson-swetnam/cloudcompare-docker
    * ...
  - [pdal offers a normal filter](https://pdal.io/en/2.6.0/stages/filters.normal.html). 
    Can this be easily scripted (for CLI usage) or is one required to write an
    adhoc CXX, build it with cmake ... ?

```bash
cd $ELAPHE_DIR
docker build -t pc2vol DockerContexts/pc2volContext
docker run --rm -v `pwd`/data:/data -it pc2vol /home/pc2vol/pc2vol/build/pc2vol -i /data/Exp-Cloud-ELAPHS-94M-sanitized-just-normals-with-CloudCompare.pts -o /data/Exp-Cloud-ELAPHS-94M-sanitized.vol
```

```bash
cd $ELAPHE_DIR
docker build -t cloudcompare DockerContexts/CloudCompareContext
docker run --rm -it cloudcompare /bin/bash
  ----> $xvfb-run /usr/local/bin/CloudCompare -SILENT
```