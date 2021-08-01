import json
import os
from pathlib import Path

key_client_name = 'client_name'
key_params = 'params'
key_success = 'success'
key_error = 'error'
key_error_type = 'error_type'
key_rid = 'rid'
key_ip = 'ip'
key_task = 'task'

key_param_first = 'first'
key_param_second = 'second'
key_param_third = 'third'

task_name_sum2 = 'sum2'
task_name_mult3 = 'mult3'
task_name_surprise = 'surprise'
api_name = 'api'

error_validation = 'validation'
error_process = 'process'

creds_file_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))), 'secret',
                               'cred.txt')
with open(creds_file_path) as f:
    creds = json.loads(f.read())
    aws_access_key_id = creds.get('aws_access_key_id')
    aws_secret_access_key = creds.get('aws_secret_access_key')

api_port = 5000

logging_dir = os.path.join(str(Path.home()), 'tasker_logs')

queue_url_sum2 = 'https://sqs.us-west-2.amazonaws.com/510208402325/sum2'
queue_url_mult3 = 'https://sqs.us-west-2.amazonaws.com/510208402325/mult3'
queue_url_surprise = 'https://sqs.us-west-2.amazonaws.com/510208402325/surprise'
