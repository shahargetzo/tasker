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


task_name_sum2 = 'sum2'
task_name_mult3 = 'mult3'
task_name_process_controller = 'process_controller'
api_name = 'api'

error_validation = 'validation'
error_process = 'process'

with open(os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'secret', 'cred.txt')) as f:
    creds = json.loads(f.read())
    aws_access_key_id = creds.get('aws_access_key_id')
    aws_secret_access_key = creds.get('aws_secret_access_key')

api_port = 5000

logging_dir = os.path.join(str(Path.home()), 'tasker', 'log')

sum2_queue_url = 'https://sqs.us-west-2.amazonaws.com/510208402325/sum2'
mult3_queue_url = 'https://sqs.us-west-2.amazonaws.com/510208402325/mult3'
