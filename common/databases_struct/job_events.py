import time

table_name = 'job_events'

key_rid = 'rid'
key_created_at = 'created_at'
key_updated_at = 'updated_at'
key_event_name = 'event_name'

primary_key_rid_event_name = f'({key_rid, key_event_name})'

db_struct = [
    {
        'name': key_rid,
        'type': 'varchar(50)'
    }, {
        'name': key_created_at,
        'type': 'bigint'
    }, {
        'name': key_updated_at,
        'type': 'bigint'
    }, {
        'name': key_event_name,
        'type': 'varchar(50)'
    }, {
        'rule': primary_key_rid_event_name
    }
]

event_name_insert_to_queue = 'insert_to_queue'
event_name_start_process = 'start_process'
event_name_end_process = 'end_process'
event_name_error_process = 'error_process'


def insert_event(data_provider, rid: str, event_name: str):
    keys = [key_rid,
            key_event_name,
            key_created_at,
            key_updated_at]
    values = (rid,
              event_name,
              time.time(),
              time.time())
    return data_provider.insert(table_name, keys, values)
