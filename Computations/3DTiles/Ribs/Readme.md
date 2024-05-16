# From Ribs outputs to 3DTiles<!-- omit from toc -->

## Table Of Content<!-- omit from toc -->

- [Generation of files](#generation-of-files)
- [Building the (docker) images](#building-the-docker-images)
- [Notational shortcuts](#notational-shortcuts)
- [For tunnel system](#for-tunnel-system)
  - [Generating the tunnel files](#generating-the-tunnel-files)
  - [Deploying the tunnel files](#deploying-the-tunnel-files)
- [For the Cave system](#for-the-cave-system)
  - [Generating the Cave files](#generating-the-cave-files)
  - [Deploying the cave files](#deploying-the-cave-files)
- [Notes](#notes)

## Generation of files

This directory illustrates how to generate the files of the
["Synthetic cave and tunnel systems" dataset](https://dataset-dl.liris.cnrs.fr/synthetic-cave-and-tunnel-systems/).
Generating those files can be done with an ad-hoc succession of docker commands.

## Building the (docker) images

Building the images boils down to
(refer to
[Ribs/Docker](https://github.com/VCityTeam/TT-Ribs/blob/master/Docker/Readme.md),
[py3dTiles/docker](https://gitlab.com/py3dtiles/py3dtiles/-/tree/main/docker),
[py3dtilers-docker](https://github.com/VCityTeam/py3dtilers-docker))

```bash
docker build -t vcity/ribs https://github.com/VCityTeam/TT-Ribs.git -f Docker/Dockerfile
docker build -t py3dtiles/py3dtiles:v7.0.0 https://gitlab.com/py3dtiles/py3dtiles.git#v7.0.0 -f docker/Dockerfile
docker build -t vcity/py3dtilers https://github.com/VCityTeam/py3dtilers-docker.git -f Context/Dockerfile
docker build -t vcity/offsetthreedtilesettolyon https://github.com/VCityTeam/UD-Reproducibility.git#master:Computations/3DTiles/Ribs/OffsetTilesetContext
```

## Notational shortcuts

```bash
alias dockerun='docker run -it --rm -v $(pwd)/data:/data'
export to_lyon_cathedral='--offset-x 1841761.4663378098 --offset-y 5175204.0252315905 --offset-z 265.1 --rename-string translated-to-lyon-cathedral'
export to_lyon_redhaired_cross='--angle-around-z -25.0 --offset-x 1842731.292340 --offset-y 5176473.016647 --offset-z 198.1 --rename-string translated-to-lyon-redhaired_cross'
```

Notes:

- the above parameters were produced through a totally manual (trial and
  error) iterative process (don't ask).
- the X axis of the tilesets are pointed towards the east: diminishing the
  "offset-x" value pulls the implantation of the tilesets towards the west.
- the Z a axis of the tilesets points towards the sky.

## For tunnel system

### Generating the tunnel files

```bash
dockerun vcity/ribs Tunnel.py --subdivision 1 --outputdir /data
dockerun py3dtiles/py3dtiles:v7.0.0 convert /data/tunnel_sub_1_point_cloud.ply --out /data/tunnel_sub_1_point_cloud-3dtiles
dockerun vcity/offsetthreedtilesettolyon  --input-dir /data/tunnel_sub_1_point_cloud-3dtiles $tunnel_to_lyon_redhaired_cross
dockerun vcity/py3dtilers obj-tiler -i /data/tunnel_sub_1_triangulation.obj --output_dir /data/tunnel_sub_1_triangulation-3dtiles
dockerun vcity/offsetthreedtilesettolyon  --input-dir /data/tunnel_sub_1_triangulation-3dtiles $tunnel_to_lyon_redhaired_cross
```

```bash
dockerun vcity/ribs Tunnel.py --subdivision 2 --outputdir /data
dockerun py3dtiles/py3dtiles:v7.0.0 convert /data/tunnel_sub_2_point_cloud.ply --out /data/tunnel_sub_2_point_cloud-3dtiles
dockerun vcity/offsetthreedtilesettolyon  --input-dir /data/tunnel_sub_2_point_cloud-3dtiles $tunnel_to_lyon_redhaired_cross
dockerun vcity/py3dtilers obj-tiler -i /data/tunnel_sub_2_triangulation.obj --output_dir /data/tunnel_sub_2_triangulation-3dtiles
dockerun vcity/offsetthreedtilesettolyon  --input-dir /data/tunnel_sub_2_triangulation-3dtiles $tunnel_to_lyon_redhaired_cross
```

```bash
dockerun vcity/ribs Tunnel.py --subdivision 3 --outputdir /data
dockerun py3dtiles/py3dtiles:v7.0.0 convert /data/tunnel_sub_3_point_cloud.ply --out /data/tunnel_sub_3_point_cloud-3dtiles
dockerun vcity/offsetthreedtilesettolyon  --input-dir /data/tunnel_sub_3_point_cloud-3dtiles $tunnel_to_lyon_redhaired_cross
dockerun vcity/py3dtilers obj-tiler -i /data/tunnel_sub_3_triangulation.obj --output_dir /data/tunnel_sub_3_triangulation-3dtiles
dockerun vcity/offsetthreedtilesettolyon  --input-dir /data/tunnel_sub_3_triangulation-3dtiles $tunnel_to_lyon_redhaired_cross
```

The following requires 64G of memory

```bash
dockerun vcity/ribs Tunnel.py --subdivision 4 --outputdir /data
dockerun py3dtiles/py3dtiles:v7.0.0 convert /data/tunnel_sub_4_point_cloud.ply --out /data/tunnel_sub_4_point_cloud-3dtiles
dockerun vcity/offsetthreedtilesettolyon  --input-dir /data/tunnel_sub_4_point_cloud-3dtiles $tunnel_to_lyon_redhaired_cross
dockerun vcity/py3dtilers obj-tiler -i /data/tunnel_sub_4_triangulation.obj --output_dir /data/tunnel_sub_4_triangulation-3dtiles
dockerun vcity/offsetthreedtilesettolyon  --input-dir /data/tunnel_sub_4_triangulation-3dtiles $tunnel_to_lyon_redhaired_cross
```

### Deploying the tunnel files

```bash
scp -r data/tunnel_sub_1_* connect:/dataset/synthetic-cave-and-tunnel-systems/Tunnel/
scp -r data/tunnel_sub_2_* connect:/dataset/synthetic-cave-and-tunnel-systems/Tunnel/
scp -r data/tunnel_sub_3_* connect:/dataset/synthetic-cave-and-tunnel-systems/Tunnel/
```

## For the Cave system

### Generating the Cave files

```bash
dockerun vcity/ribs Cave.py -v --subdivision 1 --outputdir /data
dockerun py3dtiles/py3dtiles:v7.0.0 convert /data/cave_sub_1_grid_size_x_1_grid_size_y_1_point_cloud.ply --out /data/cave_sub_1_grid_size_x_1_grid_size_y_1_point_cloud-3dtiles
dockerun vcity/offsetthreedtilesettolyon  --input-dir /data/cave_sub_1_grid_size_x_1_grid_size_y_1_point_cloud-3dtiles $to_lyon_cathedral
dockerun vcity/py3dtilers obj-tiler -i /data/cave_sub_1_grid_size_x_1_grid_size_y_1_triangulation.obj --output_dir  /data/cave_sub_1_grid_size_x_1_grid_size_y_1_triangulation-3dtiles
dockerun vcity/offsetthreedtilesettolyon  --input-dir /data/cave_sub_1_grid_size_x_1_grid_size_y_1_triangulation-3dtiles $to_lyon_cathedral
```

```bash
dockerun vcity/ribs Cave.py -v --subdivision 2 --outputdir /data
dockerun py3dtiles/py3dtiles:v7.0.0 convert /data/cave_sub_2_grid_size_x_1_grid_size_y_1_point_cloud.ply --out /data/cave_sub_2_grid_size_x_1_grid_size_y_1_point_cloud-3dtiles
dockerun vcity/offsetthreedtilesettolyon  --input-dir /data/cave_sub_2_grid_size_x_1_grid_size_y_1_point_cloud-3dtiles $to_lyon_cathedral
dockerun vcity/py3dtilers obj-tiler -i /data/cave_sub_2_grid_size_x_1_grid_size_y_1_triangulation.obj --output_dir  /data/cave_sub_2_grid_size_x_1_grid_size_y_1_triangulation-3dtiles
dockerun vcity/offsetthreedtilesettolyon  --input-dir /data/cave_sub_2_grid_size_x_1_grid_size_y_1_triangulation-3dtiles $to_lyon_cathedral
```

```bash
dockerun vcity/ribs Cave.py -v --subdivision 3 --outputdir /data
dockerun py3dtiles/py3dtiles:v7.0.0 convert /data/cave_sub_3_grid_size_x_1_grid_size_y_1_point_cloud.ply --out /data/cave_sub_3_grid_size_x_1_grid_size_y_1_point_cloud-3dtiles
dockerun vcity/offsetthreedtilesettolyon  --input-dir /data/cave_sub_3_grid_size_x_1_grid_size_y_1_point_cloud-3dtiles $to_lyon_cathedral
dockerun vcity/py3dtilers obj-tiler -i /data/cave_sub_3_grid_size_x_1_grid_size_y_1_triangulation.obj --output_dir  /data/cave_sub_3_grid_size_x_1_grid_size_y_1_triangulation-3dtiles
dockerun vcity/offsetthreedtilesettolyon  --input-dir /data/cave_sub_3_grid_size_x_1_grid_size_y_1_triangulation-3dtiles $to_lyon_cathedral
```

```bash
dockerun vcity/ribs Cave.py -v --subdivision 4 --outputdir /data
dockerun py3dtiles/py3dtiles:v7.0.0 convert /data/cave_sub_4_grid_size_x_1_grid_size_y_1_point_cloud.ply --out /data/cave_sub_4_grid_size_x_1_grid_size_y_1_point_cloud-3dtiles
dockerun vcity/offsetthreedtilesettolyon  --input-dir /data/cave_sub_4_grid_size_x_1_grid_size_y_1_point_cloud-3dtiles $to_lyon_cathedral
dockerun vcity/py3dtilers obj-tiler -i /data/cave_sub_4_grid_size_x_1_grid_size_y_1_triangulation.obj --output_dir  /data/cave_sub_4_grid_size_x_1_grid_size_y_1_triangulation-3dtiles
dockerun vcity/offsetthreedtilesettolyon  --input-dir /data/cave_sub_4_grid_size_x_1_grid_size_y_1_triangulation-3dtiles $to_lyon_cathedral
```

### Deploying the cave files

```bash
scp -r data/cave_sub_1_* connect:/dataset/synthetic-cave-and-tunnel-systems/Cave/
scp -r data/cave_sub_2_* connect:/dataset/synthetic-cave-and-tunnel-systems/Cave/
scp -r data/cave_sub_3_* connect:/dataset/synthetic-cave-and-tunnel-systems/Cave/
scp -r data/cave_sub_4_* connect:/dataset/synthetic-cave-and-tunnel-systems/Cave/
```

## Notes

- `Py3dtiles` doesn't consider the triangulations when expressed in `PLY`
- `Py3dTilers` doesn't consider point clouds when expressed in `OBJ`
