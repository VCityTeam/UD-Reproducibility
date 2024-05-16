## Usage

```bash
python3.10 -m venv venv
source venv/bin/activate
python OffsetTileset.py --input-dir ../data/tunnel_sub_3_point_cloud-3dtiles --angle-around-z -25.0 --offset-x 1842731.292340 --offset-y 5176473.016647 --offset-z 198.1 --rename-string translated-to-lyon-redhaired_cross
```

and with docker

```bash
cd $(git rev-parse --show-cdup)
cd Computations/3DTiles/Ribs/OffsetTilesetContext
docker build -t vcity/offsetthreedtilesettolyon .
dockerun vcity/offsetthreedtilesettolyon  --input-dir ../data/tunnel_sub_3_point_cloud-3dtiles --angle-around-z -25.0 --offset-x 1842731.292340 --offset-y 5176473.016647 --offset-z 198.1 --rename-string translated-to-lyon-redhaired_cross
```
