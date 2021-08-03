from src.common.service_providers.data_provider import DBWhere

table_name = 'process_config'

key_process_name = 'name'
key_created_at = 'created_at'
key_updated_at = 'updated_at'
key_status = 'status'

status_active = 'active'
status_error = 'error'
status_queue = 'queue'
status_suspended = 'suspended'

available_statuses = [
    status_active,
    status_error,
    status_suspended,
    status_queue
]


def get_process_status(data_provider, name: str):
    where = [DBWhere(key_process_name, '=', name)]
    return data_provider.get_rows(table_name, where)


def update_process_status(data_provider, name, status):
    return data_provider.update_row(table_name, {key_status: status}, {key_process_name: name})
