## Compute a 3D Tiles tileset of Lyon in 2009
The purpose of the ComputeLyon2009.sh shell script is to computes a 3D Tiles tileset representing the
buildings of Lyon for the year 2009.

The installation notes are [shared by all the applications](../Shared/Read.md#installing-dependencies) and
the running instructions are [similar to the ones of the other applications](../Shared/Read.md#running-the-worflow).
They boil down to
```
$ virtualenv -p python3 venv
$ . venv/bin/activate
(venv) pip install -r ../Shared/requirements.txt   # Because we need j2 on the cli
(venv) ./ComputeLyon2009.sh <some_output_dir>
```

