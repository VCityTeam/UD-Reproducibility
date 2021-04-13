## Things to fix
 - find so means to provide an IP-adress (to the ``demo_configuration_static.py.` configuration file)
   that is compatible with the DooD way of doing things. That is what IP-address should we provide
   so that e.g. the DB container can be accessed by the Tiler container...
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
