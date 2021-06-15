## Why this cannot work
For this [DooD](https://rusingh.com/2021/01/29/docker-outside-of-docker/) to work we need align two things

* at build time the ability to install the python pipeline in some
  directory inherent to the image (that is that can NOT be a 
  [bind-mount directory](https://docs.docker.com/storage/bind-mounts/) that
  are not available at build time).
* at run time, there is a the programatic equivalent of a `docker build`, that is 
  the script eventually calls a [DockerHelperBuild()](https://github.com/VCityTeam/UD-Reproducibility/blob/master/Computations/3DTiles/LyonTemporal/PythonCallingDocker/docker_helper.py#L59), that handles over a `path=context_dir` to the
  docker daemon. And for the docker daemon (standing outside of the running container,
  because this Dood) to be able to access to the directory holding that considered 
  (depending on the computational stage) Context, this directory must be a bind-mounted
  one (directories internal to the container are not visible from outside).

Hence the build time and run time needs contradict each other making this strategy fail :-(


### Other less serious technical details that might also have required some fixes 
In addition to Things to fix
 - find some means to provide an IP-adress (to the `demo_configuration_static.py.` configuration file)
   that is compatible with the [DooD](https://rusingh.com/2021/01/29/docker-outside-of-docker/) way of 
   doing things. That is what IP-address should we provide
   so that e.g. the DB container can be accessed by the Tiler container...
 - Probably that the [documentation for the manual steps](https://github.com/VCityTeam/UD-Reproducibility/tree/master/Computations/3DTiles/LyonTemporal/PythonCallingDocker#manual-step-by-step-run-of-the-static-tiler), that is used in the entrypoint.sh, is NOT CORRECT because
   it seems to miss the `python run_3dcitydb_server.py` launching of the database step.
 - entrypoint.sh misses the exportation of the result.

## Running things
Building the image
```
docker build -t vcity:chemistry-valley-2015 DockerContext
```
Using the container (requires "Docker Out Of Docker" a.k.a. DooD)
```
docker run -v /var/run/docker.sock:/var/run/docker.sock -t vcity:chemistry-valley-2015
```


Interactive debugging:
```
docker run -v /var/run/docker.sock:/var/run/docker.sock -it --entrypoint /bin/bash  vcity:chemistry-valley-2015
```
