# Usage

Tested with `argo version` "v3.2.2+8897fff.dirty".

Define the  required environment variable and aliases by making direnv active

```bash
ln -s envrc.tmpl .envrc
direnv allow
# and assert you are in the argo namespace (direnv should have made the job)
k config view --minify --output 'jsonpath={..namespace}'
```

Create a configmap

```bash
k apply -f simple-parameters-configmap.yaml
# Because the above command can fail without complain, check that the configmap
# was indeed created
k get configmaps simple-parameters -o yaml
```

You should now be able to use this configmap within argo:

```bash
# Check syntax of workflow
argo lint arguments-parameters-from-configmap.yaml
# The trigger the workflow (take note of the workflow ID that should be of
# the form arguments-parameters-from-configmap-<XXXXXX>
argo submit --watch arguments-parameters-from-configmap.yaml
# Then assert that the whale did say "hello world" with
argo logs arguments-parameters-from-configmap-<XXXXXX>
```

## Trouble shooting

If argo fails to access the configmap, check that the configmap is
accessible/usable at the k8s level by creating a pod that refers to this
configmap with the following command

```bash
kubeval pod-single-configmap-env-variable.yaml
k create -f pod-single-configmap-env-variable.yaml   # -v=6
# Make sure that the pod could access the configmap by checking the pod
# status that should be "Succeeded": 
k describe pod dapi-test-pod | grep Status  
# In case of trouble (e.g. a CreateContainerConfigError status) explore the
# full result of the following command (look for "Error" messages):
k describe pod dapi-test-pod
# Cleaning up failing pod
k delete pod dapi-test-pod
```

## References

Documentation:

- [Official task description](https://kubernetes.io/docs/tasks/configure-pod-container/configure-pod-configmap/)
- Full [configmap usage example](https://spectrumstutz.com/k8s/configmap-2/)
