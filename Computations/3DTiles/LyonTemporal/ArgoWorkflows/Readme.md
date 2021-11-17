# An Argo Worflows pipeline implementation test

## Running things

### Pre-requisites

```bash
brew install kubernetes-cli
kubectl version
alias k=kubectl
#
brew cask install minikube
brew install argo
# or when the above fails with "no bottle is available" then use
#      brew install --build-from-source argo
minikube --memory=8G --cpus 4 start
#
k create ns argo     # Remember the k=kubectl shell alias (refer above)
export ARGO_NAMESPACE=argo
k config set-context --current --namespace=$ARGO_NAMESPACE
# Start an argo server
k apply -f https://raw.githubusercontent.com/argoproj/argo-workflows/master/manifests/quick-start-postgres.yaml
# and assert the AW controller is running with
k get pod | grep workflow-controller
# open the ad-hoc port-forwarding
k -n argo port-forward deployment/argo-server 2746:2746 &
```

### Mount the current working directory as k8s volume

```bash
minikube mount `pwd`:/data/host &   # Note this is process (hence the ampersand)
```

A workflow can now use this as a volume (refer to 
[this example](https://minikube.sigs.k8s.io/docs/handbook/mount/)) as

```bash
"volumes": [
  {
    "name": "host-mount",
    "hostPath": {
      "path": "/data/host"
    }
  }
]
```

Hence the `minikube mount` target argument (i.e. `/data/host`) has to be
aligned with the workflow volume definition.

### Build the required containers

```bash
# User Minikube's built-in docker command, refer e.g. to
# https://stackoverflow.com/questions/42564058/how-to-use-local-docker-images-with-minikube
eval $(minikube docker-env)
docker build -t vcity:collect_lyon_data Docker/Collect-DockerContext/
```

```bash
# Because docker build can NOT use the url of sub-directory of git repository
# (refer e.g. to  
# https://stackoverflow.com/questions/25509828/can-a-docker-build-use-the-url-of-a-git-branch#27295336 )
# we designate the Dockerfile through a relative path notation (which creates
# an implicit dependency within this repository):
docker  -t vcity:3DUse ../Docker/3DUse-DockerContext/
```

### Run the pipeline

```bash
argo submit --watch --log full-workflow.yml \
            --parameter-file demo_configuration_static.yaml
```

In addition to the outputs printed at execution time, you can access to
the execution logs with

```bash
argo list logs | grep -i ^parameters-
argo logs parameters-<generated_string>
```

Notice that you can overload any of the parameters at invocation stage with

```bash
argo submit --watch --log full-workflow.yml \
   --parameter-file demo_configuration_static.yaml \
   -p pattern=BATI
```

### Troubleshooting

### Storage backend is full

When running the pipeline (with `argo submit`) you might get the following
error message

```
Error (exit code 1): failed to put file: Storage backend has reached its 
minimum free disk threshold. Please delete a few objects to proceed
```

According to
[this ansible issue](https://github.com/ansible/awx-operator/issues/609)
(with some clues from 
[this minio issue](https://github.com/minio/minio/issues/6795))
this indicates that the minikube file system is probably full. In order to free
some disk space

```bash
minikube ssh
$ docker system prune   # and hit y for yes
```

## Developers

### Install utils

```bash
# Install kub eval refer to https://www.kubeval.com/installation/
brew install kubeval
```

## The process of adapting PythonCallingDocker

### Creation of ArgoWorflows/Docker/Collect-DockerContext

Oddly enough the PythonCallingDocker version of the pipeline does not use the
container defined by LyonTemporal/Docker/Collect-DockerContext/. Instead it
choses to re-implement, in Python, the downloading process. The reason for
doing so was to be able to extend the downloading process feature with the
application of patches as well as being able to handle the directory tree
that this Python based version of the pipeline is able to propagate (or deal
with) along the different stages of the pipeline.
