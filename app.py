from flask import Flask
from flask import jsonify
from functions import *

app = Flask(__name__)
app.config.from_object('config.Configuration')


@app.route('/api/fetchJobViews', methods=['GET', 'POST'])
def fetch_job_views():
    kubernetes_dashboard_url = 'http://192.168.99.100:30000'
    job_views = []
    jobs = get_jobs()

    for namespace, namespace_jobs in jobs.items():
        for job_name, job in namespace_jobs.items():
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
