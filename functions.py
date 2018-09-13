import datetime
import math


def get_job_view(execution, prev_execution, stackstorm_url):
    """
    Gets a job view from the specified execution and previous execution
    :param execution: dict
    :param prev_execution: dict
    :param stackstorm_url: string
    :return: dict
    """

    current_time = datetime.datetime.utcnow()
    hash_code = abs(hash(execution['action']['name'])) % (10 ** 8)
    estimated_duration = ''
    prev_time_elapsed_since = ''

    if execution and 'start_timestamp' in execution:
        start_time = datetime.datetime.strptime(execution['start_timestamp'], '%Y-%m-%dT%H:%M:%S.%fZ')
        elapsed_seconds = int((current_time - start_time).total_seconds())
    else:
        elapsed_seconds = 0

    if prev_execution and 'elapsed_seconds' in prev_execution:
        prev_elapsed_seconds = int(math.ceil(prev_execution['elapsed_seconds']))
    else:
        prev_elapsed_seconds = 0

    if prev_execution:
        prev_execution_id = prev_execution['id']
        prev_build_name = prev_execution['id']

        if 'end_timestamp' in prev_execution:
            prev_end_time = datetime.datetime.strptime(prev_execution['end_timestamp'], '%Y-%m-%dT%H:%M:%S.%fZ')
            prev_time_elapsed_since = int((current_time - prev_end_time).total_seconds())

        if 'elapsed_seconds' in prev_execution:
            estimated_duration = '{}s'.format(int(math.ceil(prev_execution['elapsed_seconds'])))
    else:
        prev_execution_id = ''
        prev_build_name = ''

    prev_build_duration = estimated_duration
    progress = 0

    if execution['status'] == 'succeeded':
        status = 'successful'
    elif execution['status'] == 'failed':
        status = 'failing'
    elif execution['status'] == 'running':
        if prev_execution and prev_execution['status'] == 'failed':
            status = 'failing running'
        elif prev_execution and prev_execution['status'] == 'succeeded':
            status = 'successful running'
        else:
            status = 'unknown running'

        if prev_execution and (prev_execution['status'] == 'failed' or prev_execution['status'] == 'succeeded'):
            if prev_elapsed_seconds > 0:
                progress = int(math.floor((float(elapsed_seconds) / float(prev_elapsed_seconds)) * 100))

                if progress > 100:
                    progress = 100
            else:
                progress = 100
        else:
            progress = 100
    else:
        status = 'unknown'

    job_view = {
        'name': execution['action']['name'],
        'url': '{}/#/history/{}/general'.format(stackstorm_url, execution['id']),
        'status': status,
        'hashCode': hash_code,
        'progress': progress,
        'estimatedDuration': estimated_duration,
        'headline': '',
        'lastBuild': {
            "timeElapsedSince": str(prev_time_elapsed_since),
            "duration": prev_build_duration,
            "description": '',
            "name": prev_build_name,
            "url": '{}/#/history/{}/general'.format(stackstorm_url, prev_execution_id),
        },
        'debug': {
            'elapsed_seconds': elapsed_seconds,
            'prev_elapsed_seconds': prev_elapsed_seconds,
        }
    }

    return job_view


def grequests_exception_handler(async_request, exception):
    # print "Request failed"
    # print async_request.url
    pass


def grequests_response_handler(response, *args, **kwargs):
    # print response.url
    # print response.status_code
    # print response.text
    pass
