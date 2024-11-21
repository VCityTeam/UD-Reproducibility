# From Ribs outputs to 3DTiles<!-- omit from toc -->

## Table Of Content<!-- omit from toc -->

- [Generation of files](#generation-of-files)
- [Notational shortcuts](#notational-shortcuts)
- [Building the (docker) images](#building-the-docker-images)
- [For tunnel system](#for-tunnel-system)
  - [Generating the tunnel files](#generating-the-tunnel-files)
    - [Subdivision level 1](#subdivision-level-1)
    - [Subdivision level 2](#subdivision-level-2)
    - [Subdivision level 3](#subdivision-level-3)
    - [Subdivision level 4: requires 64G of memory](#subdivision-level-4-requires-64g-of-memory)
    - [Tunnel: additional triangulations with no boundaries](#tunnel-additional-triangulations-with-no-boundaries)
  - [Tunnel: deploying the resulting files](#tunnel-deploying-the-resulting-files)
- [For the Cave system](#for-the-cave-system)
  - [Generating the Cave files](#generating-the-cave-files)
    - [Cave: subdivision level 1](#cave-subdivision-level-1)
    - [Cave: subdivision level 2](#cave-subdivision-level-2)
    - [Cave: subdivision level 3](#cave-subdivision-level-3)
    - [Cave: subdivision level 4](#cave-subdivision-level-4)
    - [Cave: additional triangulations with no boundaries](#cave-additional-triangulations-with-no-boundaries)
  - [Cave: deploying the resulting files](#cave-deploying-the-resulting-files)
- [Notes](#notes)

## Generation of files

This directory illustrates how to generate the files of the
["Synthetic cave and tunnel systems" dataset](https://dataset-dl.liris.cnrs.fr/synthetic-cave-and-tunnel-systems/).
Generating those files can be done with an ad-hoc succession of docker commands.

## Notational shortcuts

On x86

```bash
alias docker_build='docker build'
alias docker_run='docker run -it --rm -v $(pwd)/data:/data'
```

Note that on OSX/M1-M3 the following cross building should properly build. Yet it will fail to execute (natively on AppleSilicon) because `bpy` faces this [M3-arch emulation issue](https://github.com/abiosoft/colima/issues/762#issuecomment-1896314265) on Rosetta...

```bash
alias docker_build='docker buildx build --platform=linux/amd64'
alias docker_run='docker run --platform linux/amd64 -it --rm -v $(pwd)/data:/data'
```

Additionally, if you need 3DTiles geometries with geographic coordinates (as opposed to modeling coordinates) you might wish to define

```bash
export cave_to_lyon_cathedral='--offset-x 1841761.4663378098 --offset-y 5175204.0252315905 --offset-z 265.1 --rename-string translated-to-lyon-cathedral'
export tunnel_to_lyon_redhaired_cross='--angle-around-z -25.0 --offset-x 1842731.292340 --offset-y 5176473.016647 --offset-z 198.1 --rename-string translated-to-lyon-redhaired_cross'
```

Notes:

- the above parameters were produced through a totally manual (trial and
  error) iterative process (don't ask).
- the X axis of the tilesets are pointed towards the east: diminishing the
  "offset-x" value pulls the implantation of the tilesets towards the west.
- the Z a axis of the tilesets points towards the sky.

## Building the (docker) images

Building the images boils down to
(refer to
[Ribs/Docker](https://github.com/VCityTeam/TT-Ribs/blob/master/Docker/Readme.md),
[py3dTiles/docker](https://gitlab.com/py3dtiles/py3dtiles/-/tree/main/docker),
[py3dtilers-docker](https://github.com/VCityTeam/py3dtilers-docker))

```bash
docker_build -t vcity/ribs https://github.com/VCityTeam/TT-Ribs.git -f Docker/Dockerfile
docker_build -t py3dtiles/py3dtiles:v7.0.0 https://gitlab.com/py3dtiles/py3dtiles.git#v7.0.0 -f docker/Dockerfile
docker_build -t vcity/py3dtilers https://github.com/VCityTeam/py3dtilers-docker.git -f Context/Dockerfile
docker_build -t vcity/offsetthreedtilesettolyon https://github.com/VCityTeam/UD-Reproducibility.git#master:Computations/3DTiles/Ribs/OffsetTilesetContext
```

## For tunnel system

### Generating the tunnel files

#### Subdivision level 1

```bash
docker_run vcity/ribs Tunnel.py --subdivision 1 --outputdir /data
```

```bash
docker_run py3dtiles/py3dtiles:v7.0.0 convert /data/tunnel_sub_1_point_cloud.ply --out /data/tunnel_sub_1_point_cloud-3dtiles
```

```bash
docker_run vcity/offsetthreedtilesettolyon  --input-dir /data/tunnel_sub_1_point_cloud-3dtiles $tunnel_to_lyon_redhaired_cross
```

```bash
docker_run vcity/py3dtilers obj-tiler -i /data/tunnel_sub_1_triangulation.obj --output_dir /data/tunnel_sub_1_triangulation-3dtiles
```

```bash
docker_run vcity/offsetthreedtilesettolyon  --input-dir /data/tunnel_sub_1_triangulation-3dtiles $tunnel_to_lyon_redhaired_cross
```

#### Subdivision level 2

```bash
docker_run vcity/ribs Tunnel.py --subdivision 2 --outputdir /data
```

```bash
docker_run py3dtiles/py3dtiles:v7.0.0 convert /data/tunnel_sub_2_point_cloud.ply --out /data/tunnel_sub_2_point_cloud-3dtiles
```

```bash
docker_run vcity/offsetthreedtilesettolyon  --input-dir /data/tunnel_sub_2_point_cloud-3dtiles $tunnel_to_lyon_redhaired_cross
```

```bash
docker_run vcity/py3dtilers obj-tiler -i /data/tunnel_sub_2_triangulation.obj --output_dir /data/tunnel_sub_2_triangulation-3dtiles
```

```bash
docker_run vcity/offsetthreedtilesettolyon  --input-dir /data/tunnel_sub_2_triangulation-3dtiles $tunnel_to_lyon_redhaired_cross
```

#### Subdivision level 3

```bash
docker_run vcity/ribs Tunnel.py --subdivision 3 --outputdir /data
```

```bash
docker_run py3dtiles/py3dtiles:v7.0.0 convert /data/tunnel_sub_3_point_cloud.ply --out /data/tunnel_sub_3_point_cloud-3dtiles
```

```bash
docker_run vcity/offsetthreedtilesettolyon  --input-dir /data/tunnel_sub_3_point_cloud-3dtiles $tunnel_to_lyon_redhaired_cross
```

```bash
docker_run vcity/py3dtilers obj-tiler -i /data/tunnel_sub_3_triangulation.obj --output_dir /data/tunnel_sub_3_triangulation-3dtiles
```

```bash
docker_run vcity/offsetthreedtilesettolyon  --input-dir /data/tunnel_sub_3_triangulation-3dtiles $tunnel_to_lyon_redhaired_cross
```

#### Subdivision level 4: requires 64G of memory

```bash
docker_run vcity/ribs Tunnel.py --subdivision 4 --outputdir /data
```

```bash
docker_run py3dtiles/py3dtiles:v7.0.0 convert /data/tunnel_sub_4_point_cloud.ply --out /data/tunnel_sub_4_point_cloud-3dtiles
```

```bash
docker_run vcity/offsetthreedtilesettolyon  --input-dir /data/tunnel_sub_4_point_cloud-3dtiles $tunnel_to_lyon_redhaired_cross
```

```bash
docker_run vcity/py3dtilers obj-tiler -i /data/tunnel_sub_4_triangulation.obj --output_dir /data/tunnel_sub_4_triangulation-3dtiles
```

```bash
docker_run vcity/offsetthreedtilesettolyon  --input-dir /data/tunnel_sub_4_triangulation-3dtiles $tunnel_to_lyon_redhaired_cross
```

#### Tunnel: additional triangulations with no boundaries

Here are the commands

```bash
docker_run vcity/ribs Tunnel.py -v --subdivision 1 --outputdir /data --fill_holes
docker_run vcity/ribs Tunnel.py -v --subdivision 2 --outputdir /data --fill_holes
docker_run vcity/ribs Tunnel.py -v --subdivision 3 --outputdir /data --fill_holes
docker_run vcity/ribs Tunnel.py -v --subdivision 4 --outputdir /data --fill_holes
```

and the resulting files should be of the form `data/tunnel_sub_*_no_boundaries_triangulation.obj`.

### Tunnel: deploying the resulting files

One batch submission for all levels

```bash
scp -r data/tunnel_sub_*_* connect:/dataset/synthetic-cave-and-tunnel-systems/Tunnel/
```

or each level separately

```bash
scp -r data/tunnel_sub_1_* connect:/dataset/synthetic-cave-and-tunnel-systems/Tunnel/
```

```bash
scp -r data/tunnel_sub_2_* connect:/dataset/synthetic-cave-and-tunnel-systems/Tunnel/
```

```bash
scp -r data/tunnel_sub_3_* connect:/dataset/synthetic-cave-and-tunnel-systems/Tunnel/
```

## For the Cave system

### Generating the Cave files

#### Cave: subdivision level 1

```bash
docker_run vcity/ribs Cave.py -v --subdivision 1 --outputdir /data
```

```bash
docker_run py3dtiles/py3dtiles:v7.0.0 convert /data/cave_sub_1_grid_size_x_1_grid_size_y_1_point_cloud.ply --out /data/cave_sub_1_grid_size_x_1_grid_size_y_1_point_cloud-3dtiles
```

```bash
docker_run vcity/offsetthreedtilesettolyon  --input-dir /data/cave_sub_1_grid_size_x_1_grid_size_y_1_point_cloud-3dtiles $cave_to_lyon_cathedral
```

```bash
docker_run vcity/py3dtilers obj-tiler -i /data/cave_sub_1_grid_size_x_1_grid_size_y_1_triangulation.obj --output_dir  /data/cave_sub_1_grid_size_x_1_grid_size_y_1_triangulation-3dtiles
```

```bash
docker_run vcity/offsetthreedtilesettolyon  --input-dir /data/cave_sub_1_grid_size_x_1_grid_size_y_1_triangulation-3dtiles $cave_to_lyon_cathedral
```

#### Cave: subdivision level 2

```bash
docker_run vcity/ribs Cave.py -v --subdivision 2 --outputdir /data
```

```bash
docker_run py3dtiles/py3dtiles:v7.0.0 convert /data/cave_sub_2_grid_size_x_1_grid_size_y_1_point_cloud.ply --out /data/cave_sub_2_grid_size_x_1_grid_size_y_1_point_cloud-3dtiles
```

```bash
docker_run vcity/offsetthreedtilesettolyon  --input-dir /data/cave_sub_2_grid_size_x_1_grid_size_y_1_point_cloud-3dtiles $cave_to_lyon_cathedral
```

```bash
docker_run vcity/py3dtilers obj-tiler -i /data/cave_sub_2_grid_size_x_1_grid_size_y_1_triangulation.obj --output_dir  /data/cave_sub_2_grid_size_x_1_grid_size_y_1_triangulation-3dtiles
```

```bash
docker_run vcity/offsetthreedtilesettolyon  --input-dir /data/cave_sub_2_grid_size_x_1_grid_size_y_1_triangulation-3dtiles $cave_to_lyon_cathedral
```

#### Cave: subdivision level 3

```bash
docker_run vcity/ribs Cave.py -v --subdivision 3 --outputdir /data
```

```bash
docker_run py3dtiles/py3dtiles:v7.0.0 convert /data/cave_sub_3_grid_size_x_1_grid_size_y_1_point_cloud.ply --out /data/cave_sub_3_grid_size_x_1_grid_size_y_1_point_cloud-3dtiles
```

```bash
docker_run vcity/offsetthreedtilesettolyon  --input-dir /data/cave_sub_3_grid_size_x_1_grid_size_y_1_point_cloud-3dtiles $cave_to_lyon_cathedral
```

```bash
docker_run vcity/py3dtilers obj-tiler -i /data/cave_sub_3_grid_size_x_1_grid_size_y_1_triangulation.obj --output_dir  /data/cave_sub_3_grid_size_x_1_grid_size_y_1_triangulation-3dtiles
```

```bash
docker_run vcity/offsetthreedtilesettolyon  --input-dir /data/cave_sub_3_grid_size_x_1_grid_size_y_1_triangulation-3dtiles $cave_to_lyon_cathedral
```

#### Cave: subdivision level 4

```bash
docker_run vcity/ribs Cave.py -v --subdivision 4 --outputdir /data
```

```bash
docker_run py3dtiles/py3dtiles:v7.0.0 convert /data/cave_sub_4_grid_size_x_1_grid_size_y_1_point_cloud.ply --out /data/cave_sub_4_grid_size_x_1_grid_size_y_1_point_cloud-3dtiles
```

```bash
docker_run vcity/offsetthreedtilesettolyon  --input-dir /data/cave_sub_4_grid_size_x_1_grid_size_y_1_point_cloud-3dtiles $cave_to_lyon_cathedral
```

```bash
docker_run vcity/py3dtilers obj-tiler -i /data/cave_sub_4_grid_size_x_1_grid_size_y_1_triangulation.obj --output_dir  /data/cave_sub_4_grid_size_x_1_grid_size_y_1_triangulation-3dtiles
```

```bash
docker_run vcity/offsetthreedtilesettolyon  --input-dir /data/cave_sub_4_grid_size_x_1_grid_size_y_1_triangulation-3dtiles $cave_to_lyon_cathedral
```

#### Cave: additional triangulations with no boundaries

By default the modeling of the cave is a triangulation with [boundaries](https://en.wikipedia.org/wiki/Surface_(topology)#Surfaces_with_boundary).
You might wish to run, on the cave triangulations, some algorithms that require the triangulated surface to be _without_ boundaries
(e.g. extracting the [homotopy groups generators](https://en.wikipedia.org/wiki/Fundamental_group) or the [skeleton extaction](https://doc.cgal.org/latest/Surface_mesh_skeletonization/index.html).

Here are the commands

```bash
docker_run vcity/ribs Cave.py -v --subdivision 1 --outputdir /data --fill_holes
docker_run vcity/ribs Cave.py -v --subdivision 2 --outputdir /data --fill_holes
docker_run vcity/ribs Cave.py -v --subdivision 3 --outputdir /data --fill_holes
docker_run vcity/ribs Cave.py -v --subdivision 4 --outputdir /data --fill_holes
```

and the resulting files should be of the form `data/cave_sub_*_grid_size_x_1_grid_size_y_1_no_boundaries_triangulation.obj`.

### Cave: deploying the resulting files

```bash
scp -r data/cave_sub_1_* connect:/dataset/synthetic-cave-and-tunnel-systems/Cave/
scp -r data/cave_sub_2_* connect:/dataset/synthetic-cave-and-tunnel-systems/Cave/
scp -r data/cave_sub_3_* connect:/dataset/synthetic-cave-and-tunnel-systems/Cave/
scp -r data/cave_sub_4_* connect:/dataset/synthetic-cave-and-tunnel-systems/Cave/
```

## Notes

- `Py3dtiles` doesn't consider the triangulations when expressed in `PLY`
- `Py3dTilers` doesn't consider point clouds when expressed in `OBJ`
