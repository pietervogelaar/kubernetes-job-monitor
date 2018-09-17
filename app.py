from flask import Flask
from flask import jsonify
from functions import *

app = Flask(__name__)
app.config.from_object('config.Configuration')


@app.route('/api/fetchJobViews', methods=['GET', 'POST'])
def fetch_job_views():

    if app.config['KUBERNETES_DASHBOARD_URL']:
        kubernetes_dashboard_url = app.config['KUBERNETES_DASHBOARD_URL']
    else:
        kubernetes_dashboard_url = 'http://my-kubernetes-cluster.local'

    job_views = []
    jobs = get_jobs()

    for namespace_key in sorted(jobs.keys()):
        for job_key in sorted(jobs[namespace_key].keys()):
            job = jobs[namespace_key][job_key]

            if 'prev_execution' in job:
                prev_execution = job['prev_execution']
            else:
                prev_execution = None

            job_view = get_job_view(job['execution'], prev_execution, kubernetes_dashboard_url)
            job_views.append(job_view)

    result = {
        'data': job_views,
        'meta': {
            'response_time_ms': 0,
        }
    }

    return jsonify(result)


if __name__ == "__main__":
    app.run()
