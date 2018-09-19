# Kubernetes job monitor

With Kubernetes cron jobs it's possible to execute (batch) jobs periodically. With a monitor dashboard it's
easy to see which jobs are running and if their latest status was "succeeded" or "failed".

The frontend is derived from the awesome Jenkins Build Monitor Plugin. The application uses kubectl inside
the container to retrieve the data from Kubernetes.

![Kubernetes job monitor](https://raw.githubusercontent.com/pietervogelaar/kubernetes-job-monitor/master/docs/kubernetes-job-monitor.png)

## Installation

### Kubeconfig secret

The Kubernetes job monitor uses kubectl to retrieve data from the Kubernetes cluster, which requires authentication.
The configuration for the admin user that is located at `/etc/kubernetes/admin.conf` on the Kubernetes master can be
used. It's off course also possible to create a user that only has read access to jobs (of one namespace or
all namespaces).

Convert the user configuration to one base64 encoded line:

    cat /etc/kubernetes/admin.conf | base64 | tr -d '\n'

Create the `secret.yaml` manifest:
    
    ---
    apiVersion: v1
    kind: Secret
    metadata:
      name: kubeconfig
      namespace: global
    type: Opaque
    data:
      config: thebase64encodedlinehere

Apply:

    kubectl apply -f secret.yaml

This secret will be mounted inside the container so that kubectl can use it.

### Deployment

    kubectl apply -f https://raw.githubusercontent.com/pietervogelaar/kubernetes-job-monitor/master/.kubernetes/kubernetes-job-monitor.yaml

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
