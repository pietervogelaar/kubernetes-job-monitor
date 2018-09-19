from flask import Flask
from flask import jsonify
from flask import render_template
from flask import request
from functions import *
from urllib import parse

app = Flask(__name__)
app.config.from_object('config.Configuration')

@app.route('/')
def index():
    title = request.args.get('title')

    return render_template('index.html', title=title)


@app.route('/api/fetchJobViews', methods=['GET', 'POST'])
def fetch_job_views():

    monitor_url = request.cookies.get('monitor_url')
    monitor_query_params = parse.parse_qs(parse.urlparse(monitor_url).query)

    if 'namespace' in monitor_query_params:
        namespace = monitor_query_params['namespace'][0]
    else:
        namespace = None

    if 'selector' in monitor_query_params:
        selector = monitor_query_params['selector'][0]
    else:
        selector = None

    job_views = []
    jobs = get_jobs(namespace, selector)

    for namespace_key in sorted(jobs.keys()):
        for job_key in sorted(jobs[namespace_key].keys()):
            job = jobs[namespace_key][job_key]

            if 'prev_execution' in job:
                prev_execution = job['prev_execution']
            else:
                prev_execution = None

            job_view = get_job_view(job['execution'], prev_execution, app.config['KUBERNETES_DASHBOARD_URL'])
            job_views.append(job_view)

    result = {
        'data': job_views,
        'meta': {
            'response_time_ms': 0,
        },
    }

    return jsonify(result)


if __name__ == "__main__":
    app.run()
