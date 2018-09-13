from flask import Flask
from flask import jsonify
from functions import *

app = Flask(__name__)
app.config.from_object('config.Configuration')


@app.route('/fetchJobViews', methods=['GET', 'POST'])
def fetch_job_views():
    job_views = []

    result = {
        'data': job_views,
        'meta': {
            'response_time_ms': 0,
        }
    }

    return jsonify(result)


if __name__ == "__main__":
    app.run()
