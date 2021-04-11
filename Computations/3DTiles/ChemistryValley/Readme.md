Building the image
```
docker build -t vcity:chemistry-valley-2015 DockerContext
```
Using the container (requires "Docker Out Of Docker" a.k.a. DooD)
```
docker run -v /var/run/docker.sock:/var/run/docker.sock -t vcity:chemistry-valley-2015
```
FIXME: entrypoint.sh misses the exportation of the result.


Interactive debugging:
```
docker run -v /var/run/docker.sock:/var/run/docker.sock -it --entrypoint /bin/bash  vcity:chemistry-valley-2015
```
