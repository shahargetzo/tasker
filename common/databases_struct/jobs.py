import json
import time

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

status_init = 'init'
status_done = 'done'
status_error = 'error'

db_struct = [
    {
        'name': key_rid,
        'type': 'varchar(50)',
        'rule': 'PRIMARY KEY'
    }, {
        'name': key_created_at,
        'type': 'bigint'
    }, {
        'name': key_updated_at,
        'type': 'bigint'
    }, {
        'name': key_client_name,
        'type': 'varchar(50)'
    }, {
        'name': key_status,
        'type': 'varchar(50)'
    }, {
        'name': key_error,
        'type': 'varchar(50)'
    }, {
        'name': key_task_name,
        'type': 'varchar(50)'
    }, {
        'name': key_task_params,
        'type': 'varchar(100)'
    }, {
        'name': key_result,
        'type': 'varchar(50)'
    }, {
        'name': key_client_ip,
        'type': 'varchar(50)'
    },
]


def insert_job(data_provider, rid: str, client_name: str, task_name: str, params: dict, client_ip):
    keys = [key_rid,
            key_client_name,
            key_task_name,
            key_task_params,
            key_status,
            key_created_at,
            key_updated_at,
            key_client_ip]
    values = (rid,
              client_name,
              task_name,
              json.dumps(params),
              status_init,
              time.time(),
              time.time(),
              client_ip)
    return data_provider.insert(table_name, keys, values)


def get_job_by_rid(data_provider, rid: str):
    where = [f'{key_rid} = "{rid}"']
    return data_provider.get_rows(table_name, where)


def update_job(data_provider, rid, status, result):
    to_update = {}
    if status:
        to_update[key_status] = status
    if result:
        to_update[key_result] = result
    return data_provider.update_row(table_name, to_update, {key_rid: rid})
