# [Argo Workflows](https://argoproj.github.io/argo-workflows/) testing

## References

- [Argo Workflows github hosted docs](https://argoproj.github.io/argo-workflows/)
- [Many example workflows](https://github.com/argoproj/argo-workflows/tree/master/examples)

---

## Quick starting (on OSX)

We here follow the [quick start guide](https://argoproj.github.io/argo-workflows/quick-start/), that boils down to the following commands

### Dependencies

- Install `minikube` (refer e.g. to [this guide](https://www.serverlab.ca/tutorials/containers/kubernetes/learning-kubernetes-with-minikube-on-osx/))
  
  ```bash
  brew install kubernetes-cli
  kubectl version
  brew cask install minikube
  ```

- Install [argo CLI](https://github.com/argoproj/argo-workflows/releases/tag/v3.1.11)
  
  either

  ```bash
  brew install argo
  # or when "no bottle is available"
  brew install --build-from-source argo
  ```

  or

  ```bash
  curl -sLO https://github.com/argoproj/argo-workflows/releases/download/v3.1.11/argo-darwin-amd64.gz
  gunzip argo-darwin-amd64.gz
  chmod +x argo-darwin-amd64
  mv ./argo-darwin-amd64 /usr/local/bin/argo
  argo version
  argo --help
  ```

### Starting an argo server and an associated web based UI

Start Kubernetes (4G is apparently _not_ sufficient for deploying Argo Workflow son minikube and on a desktop think of turning docker-desktop off in order to avoid "collisions")

```bash
minikube --memory=8G --cpus 4 start
```

and get some k8 syntactic confort ([kubectl cheat sheet](https://kubernetes.io/docs/reference/kubectl/cheatsheet/)) with

```bash
alias k=kubectl
# Allow for bash completions
source <(kubectl completion bash)
complete -F __start_kubectl k
# or add autocomplete permanently with
# echo "source <(kubectl completion bash)" >> ~/.bashrc 
```

Define a namespace and use it systematically

```bash
k create ns argo     # Remember the k=kubectl shell alias (refer above)
```

Configure the kubernetes (minikube) as well as the argo-CLI respective environment variables to use that namespace:

```bash
export ARGO_NAMESPACE=argo
k config set-context --current --namespace=$ARGO_NAMESPACE
```

Apply [a manifest](https://stackoverflow.com/questions/55130795/what-is-a-kubernetes-manifest) to set up an argo server

```bash
k apply -f https://raw.githubusercontent.com/argoproj/argo-workflows/master/manifests/quick-start-postgres.yaml
```

assert the AW controller is running with

```bash
k get pod | grep workflow-controller
```

and open the ad-hoc port-forwarding

```bash
k -n argo port-forward deployment/argo-server 2746:2746 &
```

in order to access argo UI by opening `https://localhost:2746` (with a web browser for which you might need to accept a "lack of https certificate" exception).

---

## Using Argo through different API

Argo can be used at different levels of API: k8s, curl, a dedicated REST API... 

### Using ArgoCLI to run an AW example workflow

Submit the workflow and watch (observe) it progress

```bash
argo submit --watch https://raw.githubusercontent.com/argoproj/argo-workflows/master/examples/hello-world.yaml
```

or submit the workflow and watch the logs on the fly

```bash
argo submit --log https://raw.githubusercontent.com/argoproj/argo-workflows/master/examples/hello-world.yaml
```

Also fool around with the UI to observe the workflow execution and the associated info.

Access to the workflow related information through the CLI

```bash
argo list           # Similar to `kubectl get wf`
argo list -v        # More verbosity: similar to `k -v6 get wf`
k -v9 get wf        # Even more verbosity
argo get @latest    # Provide more info about the last run workflow
argo logs @latest   # Provide its logs
```

### Using Argo's REST API to access the argo server

This requires an [access token](https://argoproj.github.io/argo-workflows/access-token/), which you create with

```bash
# A role is authorized to access some (limited) verbs and ressources 
k create role jenkins --verb=list,update --resource=workflows.argoproj.io 
# sa =service account
k create sa jenkins
k get sa | grep jenkins    # Just to make sure
k get sa jenkins -o yaml   # Ditto
# Bind service account with the role 
k create rolebinding jenkins --role=jenkins --serviceaccount=argo:jenkins
# Retrieve a token
SECRET=$(kubectl get sa jenkins -o=jsonpath='{.secrets[0].name}')
ARGO_TOKEN="Bearer $(kubectl get secret $SECRET -o=jsonpath='{.data.token}' | base64 --decode)"
# Just to make sure the token is indeed there
echo $ARGO_TOKEN
```

Now designate the API access point and use the token

```bash
export ARGO_SERVER=localhost:2746   # Requires the above port forwarding
argo list
```

Note: according to [this tutorial](https://youtu.be/gqfDJi7m7ng?list=PLGHfqDpnXFXLHfeapfvtt9URtUF1geuBo&t=745) it suffice to do

```bash
export ARGO_TOKEN=no
```

but this fails (and [this stackoverflow](https://stackoverflow.com/questions/66178222/accessing-argo-workflow-archive-via-http-leads-to-permission-denied-error) didn't help much).

Some REST API access related environment variables

```bash
# In the unlikely event of using many instances
export ARGO_INSTANCEID=...
export ARGO_SERVER=localhost:2746      # Do not prefix with http or https
export ARGO_SECURE=true                # Require TLS i.e. https
export ARGO_INSECURE_SKIP_VERIFY=true  # For self signed certificates
export KUBECONFIG=/dev/null            # Just to prevent any fold-back to k8s API
export ARGO_NAMESPACE=argo
export ARGO_TOKEN=...                  # Refer above
```

### Using curl to access the API

Use the UI in order to generate some demands and open your browser development tool then you can obtain the (http) requests to which the UI demand gets mapped to. Then one can retrieve such request and resubmit them with curl, and then modify/extend such request in order to suit one's need.

The (swagger generated) API docs can be retrieved on the server through https://localhost:2746/apidocs

### Using the Python wrappers

There seems to confusingly exist many sources e.g. (note that [CermakM](https://github.com/CermakM) does not seem to be contributor of the [Argo Project](https://github.com/orgs/argoproj/people) neither of [argoproj-labs](https://github.com/orgs/argoproj-labs/people) and the relationship between the [Argo Project](https://argoproj.github.io/) and [the argoproj-labs organisation](https://github.com/argoproj-labs) does not seem to be documented)

- [CermakM/argo-client-python](https://github.com/CermakM/argo-client-python) that is mirrored to [argoproj-labs/argo-client-python](https://github.com/argoproj-labs/argo-client-python)
- [CermakM/argo-python-dsl](https://github.com/CermakM/argo-python-dsl) that is mirrored to [argoproj-labs/argo-python-dsl](https://github.com/argoproj-labs/argo-python-dsl)
- [Pypi's argo-workflows-sdk](https://pypi.org/project/argo-workflows-sdk/) (mind the the trailing SDK in the name) refers to [CermakM/argo-python-dsl](https://github.com/CermakM/argo-python-dsl) (mind the trailing DSL) for its HomePage.

---
## Argo workflows running on minikube

### Mounting local directory as k8s volume

```bash
minikube mount --v 5 `pwd`:/data/host &
minikube ssh
$ ls /data/host    # OK: the content of the CWD is present
```

Note that strangely enough the volume does not appear at the
filesystem level:

```bash
$ df | grep data
$            # Empty! There is no occurrence of /data as filesystem
```

Reeferences:
- https://minikube.sigs.k8s.io/docs/handbook/persistent_volumes/
- https://minikube.sigs.k8s.io/docs/handbook/mount/
- https://stackoverflow.com/questions/54993532/how-to-use-kubernetes-persistent-local-volumes-with-minikube-on-osx

---

## Evaluation report

## Language features

### Conditional execution

- [flip-coin Source](https://github.com/argoproj/argo-workflows/blob/master/examples/coinflip-recursive.yaml)
- Testing: `argo submit --watch https://raw.githubusercontent.com/argoproj/argo-workflows/master/examples/coinflip-recursive.yaml`
- Note: conditions are expressed in Go and evaluated with [goevaluate](https://github.com/Knetic/govaluate).

### Workflow structure

Workflows can be assembled out of  

- [steps](https://github.com/argoproj/argo-workflows/tree/master/examples#steps) i.e. a linear structure (succession of steps) with the possibility for some steps to run in parallel with others: example [dag-diamond-steps.yaml](https://github.com/argoproj/argo-workflows/blob/master/examples/dag-diamond-steps.yaml)
- [tasks](https://github.com/argoproj/argo-workflows/tree/master/examples#dag) in which case the described workflows are [DAGs](https://en.wikipedia.org/wiki/Directed_acyclic_graph) (possibly with multiple roots/entry-points e.g. [dag-multiroot.yaml](https://github.com/argoproj/argo-workflows/blob/master/examples/dag-multiroot.yaml)): example [dag-daemon-task.yaml](https://github.com/argoproj/argo-workflows/blob/master/examples/dag-daemon-task.yaml)

Note: the combination of steps/tasks with conditional execution allows for **dynamic workflow structures** (that is structures that are determined along the workflow execution) refer to e.g. [dag-conditional-parameters.yaml](https://github.com/argoproj/argo-workflows/blob/master/examples/dag-conditional-parameters.yaml), [dag-enhanced-depends.yaml](https://github.com/argoproj/argo-workflows/blob/master/examples/dag-enhanced-depends.yaml) or [dag-coinflip.yaml](https://github.com/argoproj/argo-workflows/blob/master/examples/dag-coinflip.yaml)

### [Fixtures](https://en.wikipedia.org/wiki/Test_fixture#Software)

AW provides so called [daemon containers](https://github.com/argoproj/argo-workflows/tree/master/examples#daemon-containers) whose "existence can persist across multiple steps or even the entire workflow" (as opposed to so called [sidecars](https://github.com/argoproj/argo-workflows/tree/master/examples#sidecars)).

### [Iterations](https://github.com/argoproj/argo-workflows/tree/master/examples#loops)

Looping can occur on lists of items ([withItems](https://argoproj.github.io/argo-workflows/fields/#workflowstep)), lists of sets of items, on generated lists ([withParam](https://argoproj.github.io/argo-workflows/fields/#workflowstep)).

By default the execution of the tasks of the loop is done in parallel. Yet it is possible to [constrain the workflow](https://gitanswer.com/argo-workflows-execute-loop-in-sequentially-go-1000666110) with a [mutex on the task](https://github.com/argoproj/argo-workflows/blob/master/examples/synchronization-mutex-tmpl-level.yaml), in order to obain a sequetial execution.

### Parameter/artifact passing

#### Input parameters

- Parameter native types (that is within the workflow description): [objects, strings, booleans, arrays](https://argoproj.github.io/argo-workflows/core-concepts/)
- Parameter [defined within the workflow](https://github.com/argoproj/argo-workflows/blob/master/examples/arguments-parameters.yaml)
- Parameters can be overloaded (so called argument-parameter) from the CLI with
  the [`-p CLI flag`](https://github.com/argoproj/argo-workflows/blob/master/examples/arguments-parameters.yaml#L9)
- Some parameter preprocessing can be done at the workflow level through the
  usage of the
  [parameter aggregation idiom](https://github.com/argoproj/argo-workflows/blob/master/examples/parameter-aggregation.yaml)

#### Output parameters

- [artifact: files saved by a container](https://argoproj.github.io/argo-workflows/core-concepts/)

### Various language features

- [Retrying failed/errored steps](https://github.com/argoproj/argo-workflows/tree/master/examples#retrying-failed-or-errored-steps)

---

## Tasks

### Data persistence: mounting a host directory into the guest with Minikube

When developing docker containers on a desktop host, and in order to offer 
persistence (for data generated by the container), docker offers to mount a
host directory into the container through
[docker "bind mounts"](https://docs.docker.com/storage/bind-mounts/).

k8s mechanism for persistence uses the notion of
[persistent volume](https://kubernetes.io/docs/concepts/storage/persistent-volumes/).
When developing on a Minikube host (e.g. using a VM on desktop host),
[minikube is configured to persist files stored under a limited set of host directories](https://minikube.sigs.k8s.io/docs/handbook/persistent_volumes/) (e.g `/data`, `/tmp/hostpath_pv` ...). 
On OSX, and by default, a native (that is _not_ within the VM) user home
directory cannot be used to persist pod data.
But Minikube offers the
[`minikube mount <>`](https://minikube.sigs.k8s.io/docs/handbook/mount/)
to allow for a user home sub-directory (on the host native system) to be
mounted as k8s volume that pods can use to persist their data. 
