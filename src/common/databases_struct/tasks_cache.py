import time
import mysql.connector

from src.common.service_providers.data_provider import DBWhere
from src.common.utils import sql_utils

table_name = 'tasks_cache'

key_created_at = 'created_at'
key_updated_at = 'updated_at'
key_inserted_by = 'inserted_by'
key_task_name = 'task_name'
key_task_params = 'task_params'
key_result = 'result'


def insert_task(data_provider, client_name: str, task_name: str, params: dict, result):
    keys = [
        key_inserted_by,
        key_task_name,
        key_task_params,
        key_created_at,
        key_updated_at,
        key_result
    ]
    values = (
        client_name,
        task_name,
        sql_utils.dict_to_b64_str(params),
        time.time(),
        time.time(),
        result
    )
    try:
        return data_provider.insert(table_name, keys, values)
    except mysql.connector.errors.IntegrityError:
        pass


def get_result_if_exists(data_provider, task_name: str, task_params: dict):
    where = [DBWhere(key_task_name, '=', task_name),
             DBWhere(key_task_params, '=', sql_utils.dict_to_b64_str(task_params))]
    cached_task = data_provider.get_rows(table_name, where)
    if cached_task:
        cached_task = cached_task[0]
        cached_task[key_task_params] = sql_utils.b64_str_to_dict(cached_task[key_task_params])
        return cached_task
