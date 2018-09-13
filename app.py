import grequests
import requests
from flask import Flask
from flask import jsonify
from functions import *

app = Flask(__name__)
app.config.from_object('config.Configuration')


@app.route('/fetchJobViews', methods=['GET', 'POST'])
def fetch_job_views():
    job_views = []
    stackstorm_url = app.config['STACKSTORM_URL']
    stackstorm_api_url = app.config['STACKSTORM_API_URL']
    stackstorm_api_key = app.config['STACKSTORM_API_KEY']

    headers = {'St2-Api-Key': stackstorm_api_key}
    payload = {
        'exclude_attributes': 'parameters,notify',
        'pack': 'my_job'
    }

    # Get all actions
    response = requests.get('{}/actions'.format(stackstorm_api_url),
                            headers=headers,
                            params=payload)

    actions = []

    # Parse response
    if response.status_code == requests.codes.ok:
        nodes = response.json()
        for node in nodes:
            actions.append(node['name'])

    headers = {'St2-Api-Key': stackstorm_api_key}
    reqs = []

    # Create requests
    for action in actions:
        payload = {
            'exclude_attributes': 'result,trigger_instance',
            'limit': '2',
            'action': 'my_job.{}'.format(action),
        }

        reqs.append(grequests.get('{}/executions'.format(stackstorm_api_url),
                                  headers=headers,
                                  params=payload,
                                  hooks=dict(response=grequests_response_handler)))

    # Send requests (parallel)
    responses = grequests.map(reqs, exception_handler=grequests_exception_handler)
    for response in responses:
        if response:
            data = response.json()
            if len(data) > 0:
                execution = data[0]

                if len(data) > 1:
                    previous_execution = data[1]
                else:
                    previous_execution = None
            else:
                continue

            job_view = get_job_view(execution, previous_execution, stackstorm_url)
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
