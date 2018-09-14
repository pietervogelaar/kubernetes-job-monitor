import datetime
import json
import math
import subprocess
import sys


def get_job_view(execution, prev_execution, kubernetes_dashboard_url):
    """
    Gets a job view from the specified execution and previous execution
    :param execution: dict
    :param prev_execution: dict
    :param kubernetes_dashboard_url: string
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
        'url': '{}/#/history/{}/general'.format(kubernetes_dashboard_url, execution['id']),
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
            "url": '{}/#/history/{}/general'.format(kubernetes_dashboard_url, prev_execution_id),
        },
        'debug': {
            'elapsed_seconds': elapsed_seconds,
            'prev_elapsed_seconds': prev_elapsed_seconds,
        }
    }

    return job_view


def kubectl(command, output_format=None, print_output=True):
    """
    Executes kubectl commands with configured parameters
    :param command: list
    :param output_format: None Default human terminal output, but can also be json, yaml etc.
    :param print_output: bool
    :return: dict|bool
    """
    command.insert(0, 'kubectl')
    command.append('--kubeconfig=/etc/.kube/config')

    if output_format:
        command.append('--output={}'.format(output_format))

    result = exec_command(command, False, print_output)

    if result and output_format == 'json':
        return json.loads(result['stdout'])
    else:
        return result


def exec_command(command, shell=False, print_output=True):
    """
    Executes a command
    :param command: list
    :param shell: bool
    :param print_output: bool
    :return: False|dict
    """
    p = subprocess.Popen(command, shell=shell, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    stdout, stderr = p.communicate()

    # Decode byte string to string
    stdout = stdout.decode()
    stderr = stderr.decode()

    if print_output:
        # Write subprocess stdout to stdout
        sys.stdout.write(stdout)

        if stderr:
            # Write subprocess stderr to stderr
            print('stderr:')
            sys.stderr.write(stderr)

    if p.returncode > 0:
        return False
    else:
        return {
            'stdout': stdout,
            'stderr': stderr,
            'returncode': p.returncode,
        }
