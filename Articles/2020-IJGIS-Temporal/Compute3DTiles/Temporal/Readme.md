## Compute a 3D Temporal Tiles tileset of Lyon
The purpose of the ComputeLyonTemporal.sh shell script is to computes a 3D Tiles temporal tileset
representing the buildings of the city of Lyon over the three 2009, 2012, 2015 data vintages.

The installation notes are [shared by all the applications](../Shared/Readme.md#installing-dependencies) and
the running instructions are [similar to the ones of the other applications](../Shared/Readme.md#running-the-worflow).
They boil down to
```
$ virtualenv -p python3 venv
$ . venv/bin/activate
(venv) pip install -r ../Shared/requirements.txt   # Because we need j2 on the cli
(venv) ./ComputeLyonTemporal.sh <some_output_dir>
```

