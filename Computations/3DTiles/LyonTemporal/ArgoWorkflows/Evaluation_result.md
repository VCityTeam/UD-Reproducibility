# [Argo Workflows](https://argoproj.github.io/argo-workflows/) evaluation notes

## Pro and cons

## Cons

### Some kubernetes knowledge is a pre-requisite
- Because Argo Workflows (AW) is based on Kubernetes
  - Kubernetes must be known which can make the learning curve pretty steep  
  - its usage requires lots of YAML configuration files that become quickly
    pretty messy to handle

### Argo vs AirFlow

- Argo's UI is simpler (less powerful) than Airflows' UI (CLI lovers will consider that this doesn't really matter)
- Argo tasks are defined as containers which reduces ["vendor" lock issues](https://youtu.be/oXPgX7G_eow?t=684)
- If what you wish is using Airflow a Kubernetes executor then Argo's K8s mandatory dependency won't be a drawback against Argo.

### AW Caveats and limitations

- Some [workflow executors](https://argoproj.github.io/argo-workflows/workflow-executors/) can not save artifacts/parameters on the base image layer (e.g. /tmp) and must thus save them on (and thus read them from when needed, in a latter `step`/`task`) mounted volumes (refer to the [`emptyDir` workflow keyword](https://argoproj.github.io/argo-workflows/empty-dir/))
- When using a minikube host, minikube [exposes its internal docker daemon](https://stackoverflow.com/questions/42564058/how-to-use-local-docker-images-with-minikube) (other [docker daemon reference](https://stackoverflow.com/questions/52310599/what-does-minikube-docker-env-mean) ).
  We have to make sure that every k8s host offers a similar mechanism in order
  to have at hand a locally ran docker registry.
- Workflow CLI validation (`argo lint`) is far from being friendly. And IDE
  integration (that allows for syntax checking) seems
  [only possible with IntelliJ](https://docs.google.com/document/d/1BCPQx10mq4GO8x6ZRIt1XMONDxcR3OoHdBAEPYP4WiM) (starting from
  [this blog post](https://blog.argoproj.io/argo-workflows-v2-10-d20beeee5df3)
  and [with this StackOverflow](https://stackoverflow.com/questions/63650784/adding-argo-crd-validations-to-vscode)).
- Working with expressions is hell (does it work at all ?):
  References
  - The [original use case (as issue)](https://github.com/argoproj/argo-workflows/issues/4585)

## Pros

- Lots of users
- Argo-CD is well used
