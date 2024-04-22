# From Ribs outputs to 3DTiles

This directory illustrates how to generate the files of the
["Synthetic cave and tunnel systems" dataset](https://dataset-dl.liris.cnrs.fr/synthetic-cave-and-tunnel-systems/)

Generating the files can be done with docker and the process boils down to
(refer to
[Ribs/Docker](https://github.com/VCityTeam/TT-Ribs/blob/master/Docker/Readme.md),
[py3dTiles/docker](https://gitlab.com/py3dtiles/py3dtiles/-/tree/main/docker),
[py3dtilers-docker](https://github.com/VCityTeam/py3dtilers-docker))

```bash
docker build -t vcity/ribs https://github.com/VCityTeam/TT-Ribs.git -f Docker/Dockerfile
docker build -t py3dtiles/py3dtiles:v7.0.0 https://gitlab.com/py3dtiles/py3dtiles.git#v7.0.0 -f docker/Dockerfile
docker build -t vcity/py3dtilers https://github.com/VCityTeam/py3dtilers-docker.git -f Context/Dockerfile
```

```bash
docker run --rm -v $(pwd)/data:/data vcity/ribs Tunnel.py --subdivision 1 --outputdir /data
docker run --rm -v $(pwd)/data:/data py3dtiles/py3dtiles:v7.0.0 convert /data/tunnel_sub_1_point_cloud.ply --out /data/tunnel_sub_1_point_cloud-3dtiles
docker run --rm -v $(pwd)/data:/data vcity/py3dtilers obj-tiler -i /data/tunnel_sub_1_triangulation.obj --output_dir /data/tunnel_sub_1_triangulation-3dtiles
```

## Notes

The following still seems to fail for undocumented reasons

### Py3dtiles doesn't seem to consider PLY triangulations

```bash
docker run --rm -v $(pwd)/data:/data py3dtiles/py3dtiles:v7.0.0 convert /data/tunnel_sub_1_triangulation.ply --out /data/tunnel_sub_1_triangulation-3dtiles
```

### Py3dTilers doesn't seem to consider OBJ point clouds

```bash
docker run --rm -v $(pwd)/data:/data vcity/py3dtilers obj-tiler -i /data/tunnel_sub_1_point_cloud.obj --output_dir /data/tunnel_sub_1_point_cloud-3dtiles
```
