## Things to fix
 - find some means to provide an IP-adress (to the `demo_configuration_static.py.` configuration file)
   that is compatible with the [DooD](https://rusingh.com/2021/01/29/docker-outside-of-docker/) way of 
   doing things. That is what IP-address should we provide
   so that e.g. the DB container can be accessed by the Tiler container...
 - Probably that the [documentation for the manual steps](https://github.com/VCityTeam/UD-Reproducibility/tree/master/Computations/3DTiles/LyonTemporal/PythonCallingDocker#manual-step-by-step-run-of-the-static-tiler), that is used in the entrypoint.sh, is NOT CORRECT because
   it seems to miss the `python run_3dcitydb_server.py` launching of the database step.
 - entrypoint.sh misses the exportation of the result.

## Running things
Building the image

```bash
docker build -t vcity:chemistry-valley-2015 DockerContext
```

Using the container (requires "Docker Out Of Docker" a.k.a. DooD)

```bash
docker run -v /var/run/docker.sock:/var/run/docker.sock -v /tmp:/tmp -t vcity:chemistry-valley-2015
```

Interactive debugging:

```bash
docker run -v /var/run/docker.sock:/var/run/docker.sock -v /tmp:/tmp -it vcity:chemistry-valley-2015 /bin/bash
```
