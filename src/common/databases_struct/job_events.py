import time

table_name = 'job_events'

key_rid = 'rid'
key_created_at = 'created_at'
key_updated_at = 'updated_at'
key_event_name = 'event_name'

primary_key_rid_event_name = f'({key_rid, key_event_name})'

event_name_start_api_process = 'start_api'
event_name_end_api_process = 'end_api'
event_name_error_api = 'error_api'
event_name_error_api_validation = 'error_api_validation'
event_name_insert_to_queue = 'insert_to_queue'
event_name_start_process = 'start_process'
event_name_end_process = 'end_process'
event_name_error_process = 'error_process'
event_name_error_process_validation = 'error_process_validation'


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
