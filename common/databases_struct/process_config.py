table_name = 'process_config'

key_process_name = 'name'
key_created_at = 'created_at'
key_updated_at = 'updated_at'
key_status = 'status'

status_active = 'active'
status_error = 'error'
status_queue = 'queue'

db_struct = [
    {
        'name': key_process_name,
        'type': 'varchar(50)',
        'rule': 'PRIMARY KEY'
    }, {
        'name': key_created_at,
        'type': 'bigint'
    }, {
        'name': key_updated_at,
        'type': 'bigint'
    }, {
        'name': key_status,
        'type': 'varchar(50)'
    },
]


def get_process_status(data_provider, name: str):
    where = [f'{key_process_name} = {name}']
    return data_provider.get_rows(table_name, where)


def update_process_status(data_provider, name, status):
    return data_provider.update_row(table_name, {key_status: status}, {key_process_name: name})
