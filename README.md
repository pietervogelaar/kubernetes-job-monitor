# Kubernetes job monitor

With Kubernetes cron jobs it's possible to execute (batch) jobs periodically. With a monitor dashboard it's
easy to see which jobs are running and if their latest status was success or failure.

The frontend is derived from the awesome Jenkins Build Monitor Plugin. All the data is retrieved with one JSON AJAX
request to a Flask python application. The python application retrieves and combines information from kubectl into
the proper dashboard format. View the *.py files in this repository for more info.

![Kubernetes job monitor](https://hub.docker.com/r/pietervogelaar/kubernetes-job-monitor/)
