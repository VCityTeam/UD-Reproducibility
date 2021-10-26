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

### Build the required containers

```bash
# User Minikube's built-in docker command, refer e.g. to
# https://stackoverflow.com/questions/42564058/how-to-use-local-docker-images-with-minikube
eval $(minikube docker-env)
docker build -t vcity:collect_lyon_data Docker/Collect-DockerContext/
```

### Run the pipeline

```bash
argo submit --watch --log parameter.yml
# Post run log re-read (when logs got cleaned up from terminal by argo)
argo list logs | grep -i ^parameters-
argo logs parameters-<generated_string>
```

## Developers

### Install utils
```bash
# Install kub eval refer to https://www.kubeval.com/installation/
brew install kubeval
```


## The process of adapating PythonCallingDocker

### Creation of ArgoWorflows/Docker/Collect-DockerContext
Oddly enough the PythonCallingDocker version of the pipeline does not use the
containere defined by LyonTemporal/Docker/Collect-DockerContext/. Instead it
chose to re-implement, in Python, the downloading process. The reason for
doing so was to be able to extend the downloading process feature with the
application of patches as well as being able to handle the directory tree
that this Python based version of the pipeline is able to propagate (or deal
with) along the different stages of the pipeline.
