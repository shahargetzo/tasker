import json
import time

from src.common.service_providers.data_provider import DBWhere

table_name = 'jobs'

key_rid = 'rid'
key_created_at = 'created_at'
key_updated_at = 'updated_at'
key_client_name = 'client_name'
key_status = 'status'
key_error = 'error'
key_task_name = 'task_name'
key_task_params = 'task_params'
key_result = 'result'
key_client_ip = 'client_ip'
key_result_source = 'result_source'

status_init = 'init'
status_done = 'done'
status_error = 'error'

result_source_tasker = 'tasker'
result_source_cache = 'cache'


def insert_job(data_provider, rid: str, client_name: str, task_name: str, params: dict, client_ip):
    keys = [
        key_rid,
        key_client_name,
        key_task_name,
        key_task_params,
        key_status,
        key_created_at,
        key_updated_at,
        key_client_ip
    ]
    values = (
        rid,
        client_name,
        task_name,
        json.dumps(params),
        status_init,
        time.time(),
        time.time(),
        client_ip
    )
    return data_provider.insert(table_name, keys, values)


def get_job_by_rid(data_provider, rid: str):
    job = data_provider.get_rows(table_name, [DBWhere(key_rid, '=', rid)])
    if job:
        return job[0]


def update_job(data_provider, rid, status, result, result_source):
    to_update = {}
    if status:
        to_update[key_status] = status
    if result:
        to_update[key_result] = result
    if result_source:
        to_update[key_result_source] = result_source
    return data_provider.update_row(table_name, to_update, {key_rid: rid})
