# Kubernetes job monitor

With Kubernetes cron jobs it's possible to execute (batch) jobs periodically. With a monitor dashboard it's
easy to see which jobs are running and if their latest status was "succeeded" or "failed".

The frontend is derived from the awesome Jenkins Build Monitor Plugin. The application uses kubectl inside
the container to retrieve the data from Kubernetes.

![Kubernetes job monitor](https://raw.githubusercontent.com/pietervogelaar/kubernetes-job-monitor/master/docs/kubernetes-job-monitor.png)

## Installation

### Inside the cluster with a service account token (recommended)

This option is the easiest and the recommended way of installing. The Kubernetes job monitor shows all the jobs of
the cluster it is deployed to. Permissions are granted by a service account and cluster role.   

    kubectl create namespace global
    kubectl apply -f https://raw.githubusercontent.com/pietervogelaar/kubernetes-job-monitor/master/.kubernetes/kubernetes-job-monitor.yaml
    
The Kubernetes job monitor is deployed to the namespace "global", but can be anything.

**Note**: You should review the manifest above, to configure the correct host and Kubernetes dashboard URL for
deep linking.
    
### Inside a separate cluster with kubeconfig for remote monitoring

This option uses a kubeconfig file instead of a service account for permissions. A kubeconfig file can
also describe another cluster than that the Kubernetes job monitor is deployed to. So remote monitoring is possible.

The user configured in the kubeconfig file must be able to get and list batch jobs. 

Convert your kubeconfig file to one base64 encoded line:

    cat /your/.kube/config | base64 | tr -d '\n'

Create the `secret.yaml` manifest:
    
    ---
    apiVersion: v1
    kind: Secret
    metadata:
      name: kubeconfig
    type: Opaque
    data:
      config: thebase64encodedlinehere

Apply in the same namespace as the Kubernetes job monitor:

    kubectl apply -f secret.yaml

This secret will be mounted inside the container so that kubectl can use it. The apply command below deploys the
Kubernetes job monitor to the current namespace.

    kubectl apply -f https://raw.githubusercontent.com/pietervogelaar/kubernetes-job-monitor/master/.kubernetes/kubernetes-job-monitor-kubeconfig.yaml

**Note**: You should review the manifest above, to configure the correct host and Kubernetes dashboard URL for
deep linking.

## Usage

By default the Kubernetes job monitor shows the latest status of all jobs (created by cron jobs) it can find. A couple
of query parameters are available.

| Parameter | Description |
| --- | --- |
| title | The title of the monitor dashboard, which is displayed at the top and used as page title
| namespace | Show only jobs in this namespace
| selector | Show only jobs that match this selector (e.g. key1=value1,key2=value2)

### Examples

- `?namespace=namespace-a`
- `?title=My Job Monitor&namespace=namespace-a&selector=group=one`
- `?title=My Job Monitor&selector=group=two`

### Demo

    kubectl create namespace namespace-a
    kubectl create namespace namespace-b
    kubectl apply -f https://raw.githubusercontent.com/pietervogelaar/kubernetes-job-monitor/master/.kubernetes/test-cron-jobs.yaml

## References

- [https://hub.docker.com/r/pietervogelaar/kubernetes-job-monitor/](https://hub.docker.com/r/pietervogelaar/kubernetes-job-monitor/)
